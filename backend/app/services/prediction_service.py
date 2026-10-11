import json
import datetime
import os
import sys
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import pandas as pd

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.models.db_models import PredictionRecord
from ml.feature_engineering import LiveWiFiFeatureExtractor
from ml.inference import InferenceEngine
from ml.simulator import NetworkBenchmarkSimulator

class PredictionService:
    def __init__(self):
        self.feature_extractor = LiveWiFiFeatureExtractor()
        self.inference_engine = InferenceEngine()
        self.simulator = NetworkBenchmarkSimulator()

    def simulate_benchmark(self, scenario: str, custom_overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.simulator.simulate(scenario, custom_overrides)

    def process_and_predict(
        self,
        db: Session,
        recent_df: pd.DataFrame,
        latest_telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculates rolling features and produces honest 30-minute prediction."""
        engineered = self.feature_extractor.compute_features(recent_df)
        pred_result = self.inference_engine.predict_wifi_deployment(engineered, latest_telemetry)

        timestamp_str = latest_telemetry["timestamp"]
        session_id = latest_telemetry["session_id"]

        # Persist prediction record
        record = PredictionRecord(
            timestamp=timestamp_str,
            session_id=session_id,
            model_version=pred_result["model_version"],
            risk_probability=pred_result.get("risk_probability"),
            prediction_state=pred_result["prediction_state"],
            threshold=pred_result.get("threshold"),
            explanation_json=json.dumps(pred_result.get("contributing_factors", []))
        )
        db.add(record)
        db.commit()

        pred_result["timestamp"] = timestamp_str
        pred_result["session_id"] = session_id
        pred_result["engineered_features"] = engineered
        return pred_result

    def get_prediction_history(self, db: Session, limit: int = 100) -> List[Dict[str, Any]]:
        """Returns recent prediction records."""
        records = db.query(PredictionRecord).order_by(PredictionRecord.id.desc()).limit(limit).all()
        results = []
        for r in reversed(records):
            results.append({
                "timestamp": r.timestamp,
                "risk_probability": r.risk_probability,
                "prediction_state": r.prediction_state,
                "model_version": r.model_version
            })
        return results
