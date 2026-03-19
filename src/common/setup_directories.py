import fastf1
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
CACHE_DIR = PROJECT_ROOT / 'data' / 'cache'
RAW_DIR = PROJECT_ROOT / 'data' / 'raw'
PROCESSED_DIR = PROJECT_ROOT / 'data' / 'processed'
FEATURES_DIR = PROJECT_ROOT / 'data' / 'features'

# Data config
START_YEAR = 2023
END_YEAR = 2025

def setup_directories() -> None:
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f'Error occurred while creating {CACHE_DIR}: {e}')

    try:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f'Error occurred while creating {RAW_DIR}: {e}')

    try:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f'Error occurred while creating {PROCESSED_DIR}: {e}')

    try:
        FEATURES_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise RuntimeError(f'Error occurred while creating {FEATURES_DIR}: {e}')

    print('All directories created successfully!')
    
def setup_cache() -> None:
    fastf1.Cache.enable_cache(CACHE_DIR)

if __name__ == "__main__": 
    setup_directories()
