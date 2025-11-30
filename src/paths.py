# src/paths.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
NPY_DIR = DATA_DIR / "npy"
DUMPS_DIR = DATA_DIR / "dumps"
RAW_DIR = DATA_DIR / "raw"

APKS_DIR = RAW_DIR / "apks"
CSV_DIR = RAW_DIR / "csv"
FEATURES_DIR = RAW_DIR / "features"

EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"
RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

SRC_DIR = PROJECT_ROOT / "src"