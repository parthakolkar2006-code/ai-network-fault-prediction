"""End-to-end smoke test verifying pipeline components."""
import pytest
import os
import json
from collectors.network_discovery import NetworkDiscovery
from ml.feature_engineering import LiveWiFiFeatureExtractor
from ml.inference import InferenceEngine

def test_full_e2e_pipeline_smoke():
    # 1. Discover telemetry
    discovery = NetworkDiscovery()
    snapshot = discovery.collect_live_snapshot()
    assert "session_id" in snapshot
    assert "timestamp" in snapshot

    # 2. Extract features
    import pandas as pd
    extractor = LiveWiFiFeatureExtractor()
    df = pd.DataFrame([snapshot])
    features = extractor.compute_features(df)
    assert isinstance(features, dict)

    # 3. Predict deployment
    engine = InferenceEngine()
    pred = engine.predict_wifi_deployment(features, snapshot)
    assert "status" in pred
    assert "prediction_state" in pred

    # 4. Check benchmark artifacts
    art_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "artifacts")
    assert os.path.exists(os.path.join(art_dir, "experiment_results.json"))
    assert os.path.exists(os.path.join(art_dir, "ablation_results.json"))
