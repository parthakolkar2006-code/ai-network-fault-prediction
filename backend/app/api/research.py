"""Research evaluation, model comparison, ablation, and curve endpoints."""
import os
import json
from fastapi import APIRouter, BackgroundTasks
from typing import Dict, Any, List

router = APIRouter(prefix="/api/research", tags=["Research"])

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml", "artifacts")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "lcore_d_network_future_fault_30m.csv")

def _load_json(filename: str, default: Any) -> Any:
    path = os.path.join(ARTIFACTS_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            return default
    return default

@router.get("/metrics")
def get_research_metrics() -> List[Dict[str, Any]]:
    """Returns actual model comparison table generated from real ML training."""
    results = _load_json("experiment_results.json", None)
    if results is None:
        return []
    return results

@router.get("/curves")
def get_research_curves() -> Dict[str, Any]:
    """Returns ROC curves, PR curves, and threshold curves."""
    curves = _load_json("curves_data.json", {})
    thresholds = _load_json("thresholds_data.json", {})
    return {
        "curves": curves,
        "thresholds": thresholds
    }

@router.get("/feature-importance")
def get_feature_importance() -> List[Dict[str, Any]]:
    """Returns ranked feature importance / SHAP values."""
    return _load_json("feature_importance.json", [])

@router.get("/ablation")
def get_ablation_results() -> List[Dict[str, Any]]:
    """Returns actual ablation study comparing ICMP, SNMP, Interface, and Topology subsets."""
    return _load_json("ablation_results.json", [])

@router.post("/retrain")
def trigger_research_training(background_tasks: BackgroundTasks) -> Dict[str, str]:
    import sys
    if BACKEND_DIR not in sys.path:
        sys.path.insert(0, BACKEND_DIR)
    from ml.train import run_training_pipeline
    from ml.ablation import run_ablation_study

    def task():
        run_training_pipeline(DATA_PATH, ARTIFACTS_DIR)
        run_ablation_study(DATA_PATH, ARTIFACTS_DIR)

    background_tasks.add_task(task)
    return {"status": "Training initiated in background"}
