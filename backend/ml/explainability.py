"""
Explainable AI (XAI) engine using SHAP and Feature Importance / Coefficients.
Translates mathematical model contributions into interpretable network diagnostics.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional

class ModelExplainer:
    """Provides local and global explanations for benchmark and live models."""
    def __init__(self, model: Any, preprocessor: Any, feature_names: List[str]):
        self.model = model
        self.preprocessor = preprocessor
        self.feature_names = feature_names
        self.shap_explainer = None
        self._init_explainer()

    def _init_explainer(self):
        try:
            import shap
            # For tree-based models
            if hasattr(self.model, "tree_") or hasattr(self.model, "estimators_"):
                self.shap_explainer = shap.TreeExplainer(self.model)
            elif "XGB" in type(self.model).__name__ or "LGBM" in type(self.model).__name__:
                self.shap_explainer = shap.TreeExplainer(self.model)
        except Exception as e:
            # Fallback to feature importance or coefficients
            self.shap_explainer = None

    def get_global_importance(self, top_k: int = 20) -> List[Dict[str, Any]]:
        """Returns global feature importance ranked from highest to lowest."""
        importances = []
        if hasattr(self.model, "feature_importances_"):
            vals = self.model.feature_importances_
            for name, val in zip(self.feature_names, vals):
                importances.append({"feature": name, "importance": round(float(val), 5)})
        elif hasattr(self.model, "coef_"):
            vals = np.abs(self.model.coef_[0])
            for name, val in zip(self.feature_names, vals):
                importances.append({"feature": name, "importance": round(float(val), 5)})
        else:
            return []

        importances.sort(key=lambda x: x["importance"], reverse=True)
        return importances[:top_k]

    def explain_sample(self, sample_df: pd.DataFrame, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Explains an individual prediction sample.
        Returns top contributing factors with direction (+ pushes risk up, - pushes risk down).
        """
        try:
            X_trans = self.preprocessor.transform(sample_df)
            if self.shap_explainer is not None:
                shap_vals = self.shap_explainer.shap_values(X_trans)
                # If binary classification with list of 2 classes
                if isinstance(shap_vals, list) and len(shap_vals) == 2:
                    vals = shap_vals[1][0]
                elif isinstance(shap_vals, np.ndarray) and len(shap_vals.shape) == 2:
                    vals = shap_vals[0]
                else:
                    vals = shap_vals[0]
            elif hasattr(self.model, "coef_"):
                vals = self.model.coef_[0] * X_trans[0]
            elif hasattr(self.model, "feature_importances_"):
                # Approximate local contribution by scaling feature importance with normalized deviation
                vals = self.model.feature_importances_ * X_trans[0]
            else:
                return []

            contributions = []
            for name, val in zip(self.feature_names, vals):
                raw_val = sample_df[name].iloc[0] if name in sample_df else None
                contributions.append({
                    "feature": name,
                    "impact": round(float(val), 4),
                    "value": round(float(raw_val), 3) if raw_val is not None and not pd.isna(raw_val) else "N/A",
                    "direction": "INCREASES_RISK" if val > 0 else "DECREASES_RISK"
                })

            contributions.sort(key=lambda x: abs(x["impact"]), reverse=True)
            return contributions[:top_k]
        except Exception as e:
            return [{"feature": "Analysis", "impact": 0.0, "value": "Error", "direction": str(e)}]
