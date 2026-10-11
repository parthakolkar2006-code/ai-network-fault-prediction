"""FastAPI endpoint integration tests using TestClient."""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ONLINE"

def test_network_status_endpoint():
    res = client.get("/api/network/status")
    assert res.status_code == 200
    data = res.json()
    assert "connection_state" in data

def test_telemetry_current_endpoint():
    res = client.get("/api/telemetry/current")
    assert res.status_code == 200

def test_telemetry_history_endpoint():
    res = client.get("/api/telemetry/history?timeframe=1h")
    assert res.status_code == 200
    assert "data" in res.json()

def test_prediction_current_endpoint():
    res = client.get("/api/prediction/current")
    assert res.status_code == 200
    data = res.json()
    assert "prediction_state" in data

def test_model_info_endpoint():
    res = client.get("/api/model/info")
    assert res.status_code == 200
    data = res.json()
    assert "research_benchmark_model" in data
    assert "wifi_deployment_model" in data

def test_dataset_info_endpoint():
    res = client.get("/api/dataset/info")
    assert res.status_code == 200
    data = res.json()
    assert data["model_rows"] == 22381
    assert data["positive_rows"] == 1111

def test_research_metrics_endpoint():
    res = client.get("/api/research/metrics")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 5

def test_research_ablation_endpoint():
    res = client.get("/api/research/ablation")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 5
