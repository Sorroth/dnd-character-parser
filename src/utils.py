from pathlib import Path

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def validate_json_file(filepath):
    """Check if file exists and has .json extension."""
    path = Path(filepath)
    return path.exists() and path.suffix == '.json' 