"""Tests for chronological split and embargo mechanism."""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from ml.split import chronological_embargo_split

def test_chronological_embargo_split():
    # Synthetic time series with 100 minutes
    start = datetime(2025, 1, 1, 12, 0, 0)
    times = [start + timedelta(minutes=i) for i in range(100)]
    df = pd.DataFrame({
        "timestamp": times,
        "feature_1": range(100),
        "future_fault_30m": [0 if i % 10 != 0 else 1 for i in range(100)]
    })

    train_df, val_df, test_df, info = chronological_embargo_split(
        df, timestamp_col="timestamp", target_col="future_fault_30m",
        train_ratio=0.6, val_ratio=0.2, embargo_minutes=10
    )

    # Check temporal ordering
    assert train_df["timestamp"].max() < val_df["timestamp"].min()
    assert val_df["timestamp"].max() < test_df["timestamp"].min()

    # Check embargo gap
    train_val_gap = (val_df["timestamp"].min() - train_df["timestamp"].max()).total_seconds() / 60
    val_test_gap = (test_df["timestamp"].min() - val_df["timestamp"].max()).total_seconds() / 60
    assert train_val_gap >= 10
    assert val_test_gap >= 10
