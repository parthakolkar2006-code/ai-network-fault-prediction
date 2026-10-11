"""Prediction and Explainable AI REST endpoints."""
from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from ..database.session import get_db
from ..services.prediction_service import PredictionService
from ..schemas.prediction_schemas import (
    PredictionCurrentResponse,
    PredictionHistoryResponse,
    SimulationRequest,
    SimulationResponse
)

router = APIRouter(prefix="/api/prediction", tags=["Prediction"])
prediction_service = PredictionService()

@router.get("/current")
def get_current_prediction() -> Dict[str, Any]:
    from ..main import global_state
    latest = global_state.get("latest_prediction")
    if not latest:
        return {
            "timestamp": "",
            "session_id": "",
            "is_model_trained": False,
            "status": "COLLECTING_BASELINE",
            "message": "Collecting baseline telemetry for deployment model.",
            "risk_probability": None,
            "prediction_state": "BASELINE_COLLECTION",
            "threshold": None,
            "model_version": "v0.1-baseline-collector",
            "network_health_indicator": "STABLE",
            "contributing_factors": [
                {"feature": "Data Collection", "impact": 0.0, "value": "Gathering real Wi-Fi samples", "direction": "COLLECTING"}
            ]
        }
    return latest

@router.get("/history")
def get_prediction_history(db: Session = Depends(get_db)) -> Dict[str, Any]:
    hist = prediction_service.get_prediction_history(db, limit=100)
    return {
        "model_version": "v0.1-baseline-collector",
        "total_points": len(hist),
        "data": hist
    }

@router.post("/simulate", response_model=SimulationResponse)
def simulate_scenario(req: SimulationRequest) -> Dict[str, Any]:
    """
    Executes an LCORE-D Research Benchmark Simulation for a given preset:
    'healthy', 'moderate', or 'severe'.
    Returns actual ML model risk score, predicted state, threshold, and XAI factors.
    """
    try:
        return prediction_service.simulate_benchmark(req.scenario, req.custom_overrides)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation execution failed: {str(e)}"
        )

@router.post("/benchmark-test")
def test_benchmark_prediction(sample_data: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Allows testing research benchmark inference using an LCORE-D sample record or scenario."""
    try:
        if "scenario" in sample_data:
            return prediction_service.simulate_benchmark(
                sample_data["scenario"],
                sample_data.get("custom_overrides")
            )
        pred = prediction_service.inference_engine.predict_benchmark_sample(sample_data)
        if "error" in pred:
            raise HTTPException(status_code=500, detail=pred["error"])
        return pred
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark inference failed: {str(e)}")

