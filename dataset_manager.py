import pandas as pd
import os
from pathlib import Path

DATASETS_DIR = "/cleanvul_test/datasets"

DATASET_FILES = {
    "vulnscore_0": f"{DATASETS_DIR}/CleanVul_vulnscore_0.csv",
    "vulnscore_1": f"{DATASETS_DIR}/CleanVul_vulnscore_1.csv",
    "vulnscore_2": f"{DATASETS_DIR}/CleanVul_vulnscore_2.csv",
    "vulnscore_3": f"{DATASETS_DIR}/CleanVul_vulnscore_3.csv",
    "vulnscore_4": f"{DATASETS_DIR}/CleanVul_vulnscore_4.csv"
}

def load_cleanvul_dataset(dataset_name):
    """Load a specific CleanVul dataset"""
    if dataset_name not in DATASET_FILES:
        print(f"Available datasets: {list(DATASET_FILES.keys())}")
        return None
    
    file_path = DATASET_FILES[dataset_name]
    if not os.path.exists(file_path):
        print(f"Dataset file not found: {file_path}")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {dataset_name} dataset: {len(df)} rows")
        return df
    except Exception as e:
        print(f"Error loading {dataset_name}: {e}")
        return None

def explore_datasets():
    """Explore all available datasets"""
    print("CleanVul Datasets Overview:")
    print("-" * 40)
    
    for name, path in DATASET_FILES.items():
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                print(f"{name.upper()}: {len(df)} rows, {len(df.columns)} columns")
                print(f"  Columns: {list(df.columns)}")
                print()
            except:
                print(f"{name.upper()}: Error reading file")
        else:
            print(f"{name.upper()}: File not found")

def get_vulnerable_samples(dataset_name, limit=10):
    """Get vulnerable code samples from a dataset"""
    df = load_cleanvul_dataset(dataset_name)
    if df is None:
        return []
    
    vulnerable_samples = df[df.get('vulnerable', df.get('label', 0)) == 1].head(limit)
    return vulnerable_samples
