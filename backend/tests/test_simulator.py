import pytest
from fastapi.testclient import TestClient
from app.main import app
from ml.simulator import NetworkBenchmarkSimulator

client = TestClient(app)

def test_simulator_engine_presets():
    sim = NetworkBenchmarkSimulator()
    for preset in ["healthy", "moderate", "severe"]:
        res = sim.simulate(preset)
        assert res["scenario"] == preset
        assert "risk_probability" in res
        assert 0.0 <= res["risk_probability"] <= 1.0
        assert res["threshold"] > 0
        assert res["prediction_state"] in ["NORMAL", "WATCH", "ELEVATED", "HIGH RISK"]
        assert len(res["contributing_factors"]) > 0
        assert "key_metrics_summary" in res
        assert res["raw_features_count"] == 79

def test_simulator_custom_overrides():
    sim = NetworkBenchmarkSimulator()
    res = sim.simulate("healthy", custom_overrides={"icmp_loss_mean": 99.0})
    assert res["key_metrics_summary"]["icmp_loss_pct"] == 99.0

def test_simulator_api_simulate_endpoint():
    resp = client.post("/api/prediction/simulate", json={"scenario": "moderate"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["scenario"] == "moderate"
    assert "risk_probability" in data
    assert "key_metrics_summary" in data

def test_benchmark_test_endpoint_with_scenario():
    resp = client.post("/api/prediction/benchmark-test", json={"scenario": "severe"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["scenario"] == "severe"
    assert data["risk_probability"] > 0.5
