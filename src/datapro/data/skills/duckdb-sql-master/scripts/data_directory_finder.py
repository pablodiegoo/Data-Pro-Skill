from pathlib import Path
from typing import Union


def find_data_directory(
    data_dir_name: str = 'data',
    start_path: Union[str, Path] = None,
    max_levels: int = 10
) -> Path:
    """
    Find the data directory by searching upward from the current file location.
    
    Useful for notebooks and scripts that may be run from different locations
    in the project hierarchy.
    
    Parameters
    ----------
    data_dir_name : str, default='data'
        Name of the data directory to search for
    start_path : str or Path, optional
        Starting path for the search. If None, uses the location of the calling file.
        Use __file__ when calling from a script.
    max_levels : int, default=10
        Maximum number of parent directories to search
    
    Returns
    -------
    Path
        Path object pointing to the data directory
        
    Raises
    ------
    FileNotFoundError
        If data directory is not found within max_levels
        
    Examples
    --------
    >>> # From a script
    >>> from pathlib import Path
    >>> data_dir = find_data_directory(start_path=Path(__file__))
    >>> df = pd.read_csv(data_dir / 'my_data.csv')
    
    >>> # From a notebook (search from current directory)
    >>> data_dir = find_data_directory(start_path=Path.cwd())
    
    >>> # Custom data directory name
    >>> data_dir = find_data_directory(data_dir_name='datasets')
    
    Notes
    -----
    - Searches recursively in parent directories
    - Stops at the first match found
    - Useful for maintaining flexible project structures
    """
    if start_path is None:
        # Try to get the caller's file location
        import inspect
        frame = inspect.currentframe().f_back
        caller_file = frame.f_code.co_filename
        start_path = Path(caller_file).resolve().parent
    else:
        start_path = Path(start_path).resolve()
        if start_path.is_file():
            start_path = start_path.parent
    
    # Search upward through parent directories
    current_dir = start_path
    for _ in range(max_levels):
        # Look for data directory in current location
        candidates = list(current_dir.rglob(data_dir_name))
        data_dirs = [d for d in candidates if d.is_dir()]
        
        if data_dirs:
            # Return the first match
            return data_dirs[0]
        
        # Move up one level
        parent = current_dir.parent
        if parent == current_dir:
            # Reached filesystem root
            break
        current_dir = parent
    
    raise FileNotFoundError(
        f"Cannot find data directory with name '{data_dir_name}' "
        f"within {max_levels} levels from {start_path}"
    )


def get_data_path(filename: str, data_dir_name: str = 'data', start_path: Union[str, Path] = None) -> Path:
    """
    Get the full path to a data file.
    
    Convenience function that combines find_data_directory with file path construction.
    
    Parameters
    ----------
    filename : str
        Name of the data file
    data_dir_name : str, default='data'
        Name of the data directory
    start_path : str or Path, optional
        Starting path for the search
    
    Returns
    -------
    Path
        Full path to the data file
        
    Examples
    --------
    >>> data_file = get_data_path('sales.csv', start_path=Path(__file__))
    >>> df = pd.read_csv(data_file)
    """
    data_dir = find_data_directory(data_dir_name, start_path)
    return data_dir / filename


if __name__ == "__main__":
    # Example usage
    import sys
    
    print("Data Directory Finder - Examples")
    print("=" * 50)
    
    try:
        # Try to find data directory from current location
        data_dir = find_data_directory(start_path=Path.cwd())
        print(f"✓ Found data directory: {data_dir}")
        
        # List some files in the data directory
        files = list(data_dir.glob('*.csv'))[:5]
        if files:
            print(f"\nSample CSV files found:")
            for f in files:
                print(f"  - {f.name}")
        else:
            print("\nNo CSV files found in data directory")
            
    except FileNotFoundError as e:
        print(f"✗ {e}")
        print("\nThis is expected if you're not in a project with a 'data' directory")
    
    print("\n" + "=" * 50)
    print("Usage in your code:")
    print("-" * 50)
    print(\"\"\"
from pathlib import Path
import pandas as pd

# In a script
data_dir = find_data_directory(start_path=Path(__file__))
df = pd.read_csv(data_dir / 'my_data.csv')

# In a notebook
data_dir = find_data_directory(start_path=Path.cwd())
df = pd.read_csv(data_dir / 'my_data.csv')

# Or use the convenience function
data_file = get_data_path('my_data.csv', start_path=Path(__file__))
df = pd.read_csv(data_file)
\"\"\")
