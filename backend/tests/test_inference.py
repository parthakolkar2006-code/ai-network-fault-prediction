"""Tests for inference engine cold-start and research benchmark prediction."""
import pytest
from ml.inference import InferenceEngine

def test_inference_cold_start_baseline():
    engine = InferenceEngine()
    features = {"network_instability_score": 12.0}
    raw = {"gateway_latency": 15.0}

    pred = engine.predict_wifi_deployment(features, raw)
    assert pred["is_model_trained"] is False
    assert pred["status"] == "COLLECTING_BASELINE"
    assert pred["risk_probability"] is None
    assert "baseline" in pred["message"].lower()

def test_inference_research_benchmark():
    engine = InferenceEngine()
    if engine.research_artifact is not None:
        sample = {name: 0.0 for name in engine.research_artifact["feature_names"]}
        pred = engine.predict_benchmark_sample(sample)
        assert "risk_probability" in pred
        assert "prediction_state" in pred
        assert "contributing_factors" in pred
