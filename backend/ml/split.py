"""
Temporal split with embargo for LCORE-D network fault prediction dataset.
Prevents target leakage caused by overlapping 30-minute future fault windows.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from datetime import timedelta

def chronological_embargo_split(
    df: pd.DataFrame,
    timestamp_col: str = "timestamp",
    target_col: str = "future_fault_30m",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    embargo_minutes: int = 30
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Splits dataset chronologically into Train, Validation, and Test sets
    with an embargo period before split boundaries to prevent overlapping 30m target window leakage.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[timestamp_col]):
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    df = df.sort_values(timestamp_col).reset_index(drop=True)
    
    min_time = df[timestamp_col].min()
    max_time = df[timestamp_col].max()
    total_duration = max_time - min_time
    
    train_end_time = min_time + total_duration * train_ratio
    val_end_time = train_end_time + total_duration * val_ratio
    
    embargo = timedelta(minutes=embargo_minutes)
    
    # Train set: from start up to (train_end_time - embargo)
    # Samples between (train_end_time - embargo) and train_end_time are dropped from train
    # so their 30-minute future target does not span into validation period
    train_mask = df[timestamp_col] < (train_end_time - embargo)
    train_df = df[train_mask].copy()
    
    # Validation set: from train_end_time up to (val_end_time - embargo)
    val_mask = (df[timestamp_col] >= train_end_time) & (df[timestamp_col] < (val_end_time - embargo))
    val_df = df[val_mask].copy()
    
    # Test set: from val_end_time to end
    test_mask = df[timestamp_col] >= val_end_time
    test_df = df[test_mask].copy()
    
    # Summary metadata
    def get_stats(sub_df: pd.DataFrame, name: str) -> Dict[str, Any]:
        if len(sub_df) == 0:
            return {"name": name, "rows": 0, "positives": 0, "negatives": 0, "pos_rate": 0.0}
        pos = int(sub_df[target_col].sum())
        neg = len(sub_df) - pos
        return {
            "name": name,
            "rows": len(sub_df),
            "positives": pos,
            "negatives": neg,
            "pos_rate": round(pos / len(sub_df) * 100, 3),
            "start_time": str(sub_df[timestamp_col].min()),
            "end_time": str(sub_df[timestamp_col].max())
        }
    
    split_info = {
        "embargo_minutes": embargo_minutes,
        "total_rows_original": len(df),
        "total_rows_after_embargo": len(train_df) + len(val_df) + len(test_df),
        "embargo_dropped_rows": len(df) - (len(train_df) + len(val_df) + len(test_df)),
        "train": get_stats(train_df, "Train"),
        "validation": get_stats(val_df, "Validation"),
        "test": get_stats(test_df, "Test")
    }
    
    return train_df, val_df, test_df, split_info

if __name__ == "__main__":
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "lcore_d_network_future_fault_30m.csv")
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        tr, va, te, info = chronological_embargo_split(df)
        print("Split complete:")
        import json
        print(json.dumps(info, indent=2))
