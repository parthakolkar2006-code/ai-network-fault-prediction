"""Dataset audit and transparency endpoints."""
import os
import json
from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ml", "artifacts")

@router.get("/info")
def get_dataset_info() -> Dict[str, Any]:
    audit_path = os.path.join(DATA_DIR, "dataset_audit.json")
    if os.path.exists(audit_path):
        with open(audit_path, "r") as f:
            audit = json.load(f)
    else:
        audit = {
            "source": "LCORE-D v2",
            "model_rows": 22381,
            "positive_rows": 1111,
            "negative_rows": 21270,
            "positive_rate": 0.04964,
            "fault_events": 69,
            "time_start": "2025-10-12 10:50:00",
            "time_end": "2025-11-28 13:42:00",
            "columns": []
        }

    split_path = os.path.join(ARTIFACTS_DIR, "split_info.json")
    split_info = None
    if os.path.exists(split_path):
        with open(split_path, "r") as f:
            split_info = json.load(f)

    return {
        "source": audit.get("source", "LCORE-D v2"),
        "model_rows": audit.get("model_rows", 22381),
        "positive_rows": audit.get("positive_rows", 1111),
        "negative_rows": audit.get("negative_rows", 21270),
        "positive_rate": round(audit.get("positive_rate", 0.04964) * 100, 3),
        "fault_events": audit.get("fault_events", 69),
        "time_start": audit.get("time_start", "2025-10-12 10:50:00"),
        "time_end": audit.get("time_end", "2025-11-28 13:42:00"),
        "feature_count": audit.get("feature_count_excluding_timestamp_target", 79),
        "features": [c for c in audit.get("columns", []) if c not in ["timestamp", "future_fault_30m"]],
        "split_info": split_info,
        "target_definition": "future_fault_30m = 1 if a logged network fault starts within next 30 minutes; 0 otherwise. Current fault intervals excluded.",
        "leakage_prevention": "Strict chronological embargo splitting. No future rolling metrics. IP/gateway/class excluded from features."
    }
