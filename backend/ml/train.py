"""
Complete training pipeline for LCORE-D network future fault prediction models.
Evaluates 5 architectures with temporal embargo splitting, class imbalance handling,
validation threshold optimization, and comprehensive metric persistence.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
import xgboost as xgb
import lightgbm as lgb

try:
    from .split import chronological_embargo_split
    from .feature_engineering import ResearchDataPreprocessor, RESEARCH_FEATURES
    from .evaluate import calculate_metrics_at_threshold, find_optimal_threshold, generate_curve_points
    from .explainability import ModelExplainer
except ImportError:
    from ml.split import chronological_embargo_split
    from ml.feature_engineering import ResearchDataPreprocessor, RESEARCH_FEATURES
    from ml.evaluate import calculate_metrics_at_threshold, find_optimal_threshold, generate_curve_points
    from ml.explainability import ModelExplainer

def run_training_pipeline(
    data_path: str,
    artifacts_dir: str
) -> Dict[str, Any]:
    """Runs complete end-to-end training and evaluation pipeline."""
    os.makedirs(artifacts_dir, exist_ok=True)
    
    print(f"Loading research dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    # 1. Temporal split with embargo
    print("Performing chronological embargo split (70% Train, 15% Val, 15% Test)...")
    train_df, val_df, test_df, split_info = chronological_embargo_split(
        df, timestamp_col="timestamp", target_col="future_fault_30m",
        train_ratio=0.70, val_ratio=0.15, embargo_minutes=30
    )
    
    with open(os.path.join(artifacts_dir, "split_info.json"), "w") as f:
        json.dump(split_info, f, indent=2)
    
    # 2. Fit Preprocessor ONLY on training set
    preprocessor = ResearchDataPreprocessor(RESEARCH_FEATURES)
    X_train = preprocessor.fit_transform(train_df)
    y_train = train_df["future_fault_30m"].values.astype(int)
    
    X_val = preprocessor.transform(val_df)
    y_val = val_df["future_fault_30m"].values.astype(int)
    
    X_test = preprocessor.transform(test_df)
    y_test = test_df["future_fault_30m"].values.astype(int)
    
    # Positive weight for XGBoost
    neg_count = int(np.sum(y_train == 0))
    pos_count = int(np.sum(y_train == 1))
    scale_pos = (neg_count / pos_count) if pos_count > 0 else 1.0
    
    # Model candidates
    models = {
        "Logistic Regression": LogisticRegression(
            class_weight="balanced", max_iter=1000, random_state=42
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=12, class_weight="balanced_subsample",
            random_state=42, n_jobs=-1
        ),
        "HistGradientBoosting": HistGradientBoostingClassifier(
            class_weight="balanced", max_iter=100, random_state=42
        ),
        "XGBoost": xgb.XGBClassifier(
            n_estimators=100, max_depth=6, scale_pos_weight=scale_pos,
            eval_metric="logloss", random_state=42, n_jobs=-1
        ),
        "LightGBM": lgb.LGBMClassifier(
            n_estimators=100, max_depth=6, class_weight="balanced",
            random_state=42, n_jobs=-1, verbose=-1
        )
    }
    
    comparison_results = []
    trained_objects = {}
    curves_data = {}
    thresholds_data = {}
    
    best_model_name = None
    best_val_score = -1.0
    
    print("\nTraining and evaluating models...")
    for name, model in models.items():
        print(f"--> Training {name}...")
        model.fit(X_train, y_train)
        trained_objects[name] = model
        
        # Predict probabilities on validation set
        val_probs = model.predict_proba(X_val)[:, 1]
        
        # Optimize threshold on Validation set
        opt_thresh, val_metrics, val_thresh_curve = find_optimal_threshold(
            y_val, val_probs, metric="f1"
        )
        thresholds_data[name] = {
            "optimal_threshold": opt_thresh,
            "curve": val_thresh_curve
        }
        
        # Evaluate on Test set with locked optimal threshold
        test_probs = model.predict_proba(X_test)[:, 1]
        test_metrics = calculate_metrics_at_threshold(y_test, test_probs, opt_thresh)
        
        # Generate ROC / PR curve points
        curve_pts = generate_curve_points(y_test, test_probs)
        curves_data[name] = curve_pts
        
        entry = {
            "model_name": name,
            "optimal_threshold": opt_thresh,
            "test_roc_auc": test_metrics["roc_auc"],
            "test_pr_auc": test_metrics["pr_auc"],
            "test_precision": test_metrics["precision"],
            "test_recall": test_metrics["recall"],
            "test_f1": test_metrics["f1"],
            "test_f2": test_metrics["f2"],
            "test_specificity": test_metrics["specificity"],
            "test_fpr": test_metrics["false_positive_rate"],
            "test_fnr": test_metrics["false_negative_rate"],
            "confusion_matrix": {
                "tp": test_metrics["tp"],
                "fp": test_metrics["fp"],
                "fn": test_metrics["fn"],
                "tn": test_metrics["tn"]
            }
        }
        comparison_results.append(entry)
        
        # Selection criterion: Validation F1 / PR-AUC
        val_score = val_metrics.get("pr_auc", 0.0) + val_metrics.get("f1", 0.0)
        if val_score > best_val_score:
            best_val_score = val_score
            best_model_name = name
    
    print(f"\nOptimal benchmark model selected: {best_model_name}")
    best_model = trained_objects[best_model_name]
    best_thresh = thresholds_data[best_model_name]["optimal_threshold"]
    
    # Save best model artifact
    model_artifact = {
        "model": best_model,
        "preprocessor": preprocessor,
        "feature_names": RESEARCH_FEATURES,
        "threshold": best_thresh,
        "model_name": best_model_name
    }
    joblib.dump(model_artifact, os.path.join(artifacts_dir, "research_model.joblib"))
    
    # Explainer on best model
    explainer = ModelExplainer(best_model, preprocessor, RESEARCH_FEATURES)
    feature_importances = explainer.get_global_importance(top_k=25)
    
    with open(os.path.join(artifacts_dir, "feature_importance.json"), "w") as f:
        json.dump(feature_importances, f, indent=2)
    
    # Save comparison results
    with open(os.path.join(artifacts_dir, "experiment_results.json"), "w") as f:
        json.dump(comparison_results, f, indent=2)
        
    with open(os.path.join(artifacts_dir, "curves_data.json"), "w") as f:
        json.dump(curves_data, f, indent=2)
        
    with open(os.path.join(artifacts_dir, "thresholds_data.json"), "w") as f:
        json.dump(thresholds_data, f, indent=2)
        
    # Model Card
    best_metrics = [c for c in comparison_results if c["model_name"] == best_model_name][0]
    model_card = {
        "model_title": "LCORE-D Predictive Network Fault 30-Minute Benchmark",
        "selected_architecture": best_model_name,
        "version": "1.0.0",
        "optimal_threshold": best_thresh,
        "features_count": len(RESEARCH_FEATURES),
        "target": "future_fault_30m (fault starts within 30 min, current fault excluded)",
        "train_rows": split_info["train"]["rows"],
        "val_rows": split_info["validation"]["rows"],
        "test_rows": split_info["test"]["rows"],
        "test_metrics": best_metrics,
        "domain_scope": "Emulated Core ISP Network (LCORE-D v2)",
        "deployment_status": "Benchmark Only. Real Wi-Fi deployment model requires laptop telemetry collection.",
        "created_at": pd.Timestamp.now().isoformat()
    }
    with open(os.path.join(artifacts_dir, "model_card.json"), "w") as f:
        json.dump(model_card, f, indent=2)
        
    print("All research artifacts successfully generated and saved.")
    return model_card

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    d_path = os.path.join(current_dir, "..", "data", "lcore_d_network_future_fault_30m.csv")
    art_path = os.path.join(current_dir, "artifacts")
    run_training_pipeline(d_path, art_path)
