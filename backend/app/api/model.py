"""Model cards, versions, and deployment model status endpoints."""
import os
import json
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/model", tags=["Model"])

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml", "artifacts")

@router.get("/info")
def get_model_info() -> Dict[str, Any]:
    card_path = os.path.join(ARTIFACTS_DIR, "model_card.json")
    if os.path.exists(card_path):
        with open(card_path, "r") as f:
            research_card = json.load(f)
    else:
        research_card = {
            "model_title": "LCORE-D Predictive Network Fault 30-Minute Benchmark",
            "selected_architecture": "Not evaluated yet",
            "version": "1.0.0",
            "deployment_status": "Benchmark training required."
        }

    wifi_model_path = os.path.join(ARTIFACTS_DIR, "wifi_deployment_model.joblib")
    wifi_status = {
        "status": "COLLECTING_BASELINE" if not os.path.exists(wifi_model_path) else "READY",
        "description": "Real Wi-Fi deployment model collects baseline telemetry until sufficient sustained degradation events are logged.",
        "model_file_exists": os.path.exists(wifi_model_path),
        "target_definition": "future_degradation_30m (sustained latency/loss/disconnect within 30m)"
    }

    return {
        "research_benchmark_model": research_card,
        "wifi_deployment_model": wifi_status
    }
