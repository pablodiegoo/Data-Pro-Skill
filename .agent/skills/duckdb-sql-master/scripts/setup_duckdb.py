
"""
Simple utility to verify DuckDB installation and install recommended extensions.
Usage: python3 scripts/setup_duckdb.py
"""
import subprocess
import sys

def check_install():
    try:
        import duckdb
        print(f"✅ DuckDB {duckdb.__version__} is installed.")
        return True
    except ImportError:
        print("❌ DuckDB is NOT installed.")
        return False

def install_duckdb():
    print("🚀 Installing DuckDB...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "duckdb", "pandas"])
        print("✅ DuckDB installed successfully.")
    except Exception as e:
        print(f"❌ Installation failed: {e}")

def configure_extensions():
    try:
        import duckdb
        print("🔧 Installing core extensions (httpfs, spatial, icu)...")
        con = duckdb.connect()
        con.install_extension('httpfs')
        con.load_extension('httpfs')
        con.install_extension('icu')
        con.load_extension('icu')
        con.install_extension('spatial')
        con.load_extension('spatial')
        print("✅ Core extensions installed.")
    except Exception as e:
        print(f"⚠️ Extension installation warning: {e}")

if __name__ == "__main__":
    if not check_install():
        install_duckdb()
    
    if check_install():
        configure_extensions()
