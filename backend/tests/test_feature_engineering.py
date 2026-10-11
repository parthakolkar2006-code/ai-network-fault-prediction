"""Tests for live feature extraction and historical window adherence."""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from ml.feature_engineering import LiveWiFiFeatureExtractor

def test_feature_engineering_rolling_windows():
    extractor = LiveWiFiFeatureExtractor()
    start = datetime(2026, 1, 1, 10, 0, 0)
    data = []
    for i in range(15):
        data.append({
            "timestamp": start + timedelta(minutes=i),
            "gateway_latency": 10.0 + i,
            "gateway_packet_loss": 0.0,
            "gateway_jitter": 1.0,
            "internet_latency": 25.0 + i,
            "internet_packet_loss": 0.0,
            "internet_jitter": 2.0,
            "signal_strength": 90 - i,
            "download_bps": 1000000,
            "upload_bps": 500000,
            "packet_errors": 0,
            "network_disconnect_event": 0
        })
    df = pd.DataFrame(data)
    features = extractor.compute_features(df)

    assert "gateway_latency_mean_5m" in features
    assert "network_instability_score" in features
    assert "gateway_vs_internet_latency_diff" in features
    assert features["gateway_vs_internet_latency_diff"] == 15.0
