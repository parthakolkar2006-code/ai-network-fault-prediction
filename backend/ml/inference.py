"""
Unified Inference Engine for Research Benchmark and Real Laptop Wi-Fi Models.
Strictly adheres to domain shift integrity: never serves fabricated Wi-Fi predictions.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional, List

class InferenceEngine:
    def __init__(self, artifacts_dir: Optional[str] = None):
        if artifacts_dir is None:
            artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")
        self.artifacts_dir = artifacts_dir
        self.research_artifact = None
        self.wifi_deployment_artifact = None
        self._load_artifacts()

    def _load_artifacts(self):
        research_model_path = os.path.join(self.artifacts_dir, "research_model.joblib")
        if os.path.exists(research_model_path):
            try:
                self.research_artifact = joblib.load(research_model_path)
                if self.research_artifact and "preprocessor" in self.research_artifact:
                    prep = self.research_artifact["preprocessor"]
                    if hasattr(prep, "imputer") and hasattr(prep.imputer, "statistics_") and not hasattr(prep.imputer, "_fill_dtype"):
                        try:
                            prep.imputer._fill_dtype = prep.imputer.statistics_.dtype
                        except Exception:
                            pass
            except Exception as e:
                print(f"Error loading research model: {e}")

        wifi_model_path = os.path.join(self.artifacts_dir, "wifi_deployment_model.joblib")
        if os.path.exists(wifi_model_path):
            try:
                self.wifi_deployment_artifact = joblib.load(wifi_model_path)
            except Exception as e:
                print(f"Error loading wifi model: {e}")

    def predict_wifi_deployment(
        self,
        engineered_features: Dict[str, Any],
        raw_telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Inference for live laptop Wi-Fi telemetry.
        If a validated deployment model does not yet exist, returns honest cold-start state.
        """
        # Check if deployment model exists
        if self.wifi_deployment_artifact is None:
            # Baseline collection heuristic for warning indicators (non-ML health flag)
            instability = engineered_features.get("network_instability_score", 0.0)
            heuristic_status = "STABLE"
            if instability > 40.0:
                heuristic_status = "DEGRADED"

            return {
                "is_model_trained": False,
                "status": "COLLECTING_BASELINE",
                "message": "Collecting baseline telemetry for deployment model.",
                "risk_probability": None,
                "prediction_state": "BASELINE_COLLECTION",
                "threshold": None,
                "model_version": "v0.1-baseline-collector",
                "network_health_indicator": heuristic_status,
                "contributing_factors": [
                    {"feature": "Data Collection", "impact": 0.0, "value": "Gathering real Wi-Fi samples", "direction": "COLLECTING"},
                    {"feature": "Instability Score", "impact": round(instability / 100.0, 2), "value": f"{instability:.1f}/100", "direction": "MONITORING"}
                ]
            }

        # If deployment model exists, compute actual ML prediction
        try:
            model = self.wifi_deployment_artifact["model"]
            preprocessor = self.wifi_deployment_artifact["preprocessor"]
            feature_names = self.wifi_deployment_artifact["feature_names"]
            thresh = self.wifi_deployment_artifact.get("threshold", 0.5)

            df_input = pd.DataFrame([engineered_features])[feature_names]
            X_trans = preprocessor.transform(df_input)
            prob = float(model.predict_proba(X_trans)[0, 1])

            # Classify into states based on threshold
            # Normal: < 0.5 * thresh
            # Watch: 0.5 * thresh to thresh
            # Elevated: thresh to thresh + (1 - thresh)*0.5
            # High Risk: >= thresh + (1 - thresh)*0.5
            if prob < thresh * 0.5:
                state = "NORMAL"
            elif prob < thresh:
                state = "WATCH"
            elif prob < thresh + (1.0 - thresh) * 0.5:
                state = "ELEVATED"
            else:
                state = "HIGH RISK"

            return {
                "is_model_trained": True,
                "status": "PREDICTION_ACTIVE",
                "message": "Deployment inference active.",
                "risk_probability": round(prob, 4),
                "prediction_state": state,
                "threshold": round(thresh, 4),
                "model_version": self.wifi_deployment_artifact.get("version", "1.0-wifi"),
                "contributing_factors": []
            }
        except Exception as e:
            return {
                "is_model_trained": False,
                "status": "INFERENCE_ERROR",
                "message": f"Error running deployment model: {e}",
                "risk_probability": None,
                "prediction_state": "ERROR",
                "threshold": None,
                "model_version": "N/A",
                "contributing_factors": []
            }

    def predict_benchmark_sample(self, row_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Runs inference using the LCORE-D research benchmark model."""
        if self.research_artifact is None:
            return {
                "error": "Research model not trained yet. Run train.py first."
            }

        model = self.research_artifact["model"]
        preprocessor = self.research_artifact["preprocessor"]
        feature_names = self.research_artifact["feature_names"]
        thresh = self.research_artifact.get("threshold", 0.5)

        df_sample = pd.DataFrame([row_dict])
        for feat in feature_names:
            if feat not in df_sample.columns:
                df_sample[feat] = 0.0
        df_sample = df_sample[feature_names]
        X_trans = preprocessor.transform(df_sample)
        prob = float(model.predict_proba(X_trans)[0, 1])

        if prob < thresh * 0.5:
            state = "NORMAL"
        elif prob < thresh:
            state = "WATCH"
        elif prob < thresh + (1.0 - thresh) * 0.5:
            state = "ELEVATED"
        else:
            state = "HIGH RISK"

        try:
            from .explainability import ModelExplainer
        except ImportError:
            from ml.explainability import ModelExplainer
        explainer = ModelExplainer(model, preprocessor, feature_names)
        factors = explainer.explain_sample(df_sample, top_k=5)

        return {
            "model_name": self.research_artifact.get("model_name", "Research Model"),
            "risk_probability": round(prob, 4),
            "prediction_state": state,
            "threshold": round(thresh, 4),
            "contributing_factors": factors
        }
