# mypackage/data_loading.py
from datasets import load_dataset

def load_data():
    ds = load_dataset("deepmind/aqua_rat", "raw")
    return ds['train']