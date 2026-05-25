
import duckdb
import pandas as pd
import os
from typing import Union, List, Optional

class DataEngine:
    """
    Core data engine using DuckDB for high-performance localized OLAP.
    Acts as the primary 'motor' for reading CSVs and processing survey data.
    """
    
    def __init__(self, db_path: str = ":memory:"):
        self.con = duckdb.connect(db_path)
        self._setup_extensions()

    def _setup_extensions(self):
        """Install and load necessary extensions."""
        try:
            self.con.install_extension('httpfs')
            self.con.load_extension('httpfs')
            self.con.install_extension('icu')
            self.con.load_extension('icu')
        except Exception as e:
            # Silently fail if extensions can't be loaded (e.g. no internet)
            pass

    def load_data(self, file_path: str, table_name: str, view: bool = False):
        """
        Loads a file (CSV, Parquet, JSON) into DuckDB.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        cmd = "VIEW" if view else "TABLE"
        
        if ext == '.csv':
            query = f"CREATE OR REPLACE {cmd} {table_name} AS SELECT * FROM read_csv_auto('{file_path}')"
        elif ext == '.parquet':
            query = f"CREATE OR REPLACE {cmd} {table_name} AS SELECT * FROM read_parquet('{file_path}')"
        elif ext == '.json':
            query = f"CREATE OR REPLACE {cmd} {table_name} AS SELECT * FROM read_json_auto('{file_path}')"
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
        self.con.execute(query)

    def query(self, sql: str) -> pd.DataFrame:
        """Executes a SQL query and returns a Pandas DataFrame."""
        return self.con.execute(sql).df()

    def process_survey_logic(self, table_name: str, config: dict):
        """
        Applies common survey logic (normalizations, domain scores) using SQL via DuckDB.
        """
        # 1. Handle Normalizations
        if "normalizations" in config:
            for norm_col, settings in config["normalizations"].items():
                cols = settings["columns"]
                max_p = settings["max_points"]
                scale = settings["scale_to"]
                
                if isinstance(cols, dict):
                    sql_parts = []
                    for col, weight in cols.items():
                        sql_parts.append(f"(CASE WHEN CAST(COALESCE(\"{col}\", '0') AS VARCHAR) NOT IN ('', '0', 'nan', 'None') THEN {weight} ELSE 0 END)")
                    
                    points_calc = " + ".join(sql_parts)
                    self.con.execute(f"ALTER TABLE {table_name} ADD COLUMN \"{norm_col}\" DOUBLE")
                    self.con.execute(f"UPDATE {table_name} SET \"{norm_col}\" = (({points_calc}) / {max_p}) * {scale}")

        # 2. Handle Domains
        if "domains" in config:
            for domain_name, cols in config["domains"].items():
                col_list = ", ".join([f"CAST(COALESCE(\"{c}\", 0) AS DOUBLE)" for c in cols])
                self.con.execute(f"ALTER TABLE {table_name} ADD COLUMN \"{domain_name}\" DOUBLE")
                self.con.execute(f"UPDATE {table_name} SET \"{domain_name}\" = ({col_list}) / {len(cols)}")

    def export(self, table_or_query: str, output_path: str):
        """Exports data to Parquet or CSV based on extension."""
        ext = os.path.splitext(output_path)[1].lower()
        if table_or_query.strip().lower().startswith("select"):
            source = f"({table_or_query})"
        else:
            source = table_or_query
            
        if ext == '.parquet':
            query = f"COPY {source} TO '{output_path}' (FORMAT 'PARQUET')"
        else:
            query = f"COPY {source} TO '{output_path}' (HEADER, DELIMITER ',')"
            
        self.con.execute(query)

    def close(self):
        self.con.close()
