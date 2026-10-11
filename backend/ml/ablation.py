"""
Ablation Study for telemetry feature subsets.
Measures actual incremental contributions of ICMP, SNMP, Interface, and Topology telemetry.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from typing import Dict, Any, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

try:
    from .split import chronological_embargo_split
    from .feature_engineering import ResearchDataPreprocessor, RESEARCH_FEATURES
    from .evaluate import calculate_metrics_at_threshold, find_optimal_threshold
except ImportError:
    from ml.split import chronological_embargo_split
    from ml.feature_engineering import ResearchDataPreprocessor, RESEARCH_FEATURES
    from ml.evaluate import calculate_metrics_at_threshold, find_optimal_threshold
import lightgbm as lgb

def run_ablation_study(data_path: str, artifacts_dir: str) -> List[Dict[str, Any]]:
    print(f"Loading data for ablation study from {data_path}...")
    df = pd.read_csv(data_path)
    
    train_df, val_df, test_df, _ = chronological_embargo_split(
        df, timestamp_col="timestamp", target_col="future_fault_30m",
        train_ratio=0.70, val_ratio=0.15, embargo_minutes=30
    )
    
    y_train = train_df["future_fault_30m"].values.astype(int)
    y_val = val_df["future_fault_30m"].values.astype(int)
    y_test = test_df["future_fault_30m"].values.astype(int)
    
    # Feature subsets
    icmp_features = [c for c in RESEARCH_FEATURES if "icmp" in c or "ping" in c or "response_time" in c]
    icmp_snmp_features = icmp_features + [c for c in RESEARCH_FEATURES if "snmp" in c or "uptime" in c]
    icmp_snmp_interface_features = icmp_snmp_features + [c for c in RESEARCH_FEATURES if "interface" in c or "bits" in c]
    all_telemetry_features = [c for c in RESEARCH_FEATURES if not c.startswith("r")]
    all_telemetry_plus_router = RESEARCH_FEATURES

    subsets = {
        "ICMP-only features": icmp_features,
        "ICMP + SNMP": list(set(icmp_snmp_features)),
        "ICMP + SNMP + Interface metrics": list(set(icmp_snmp_interface_features)),
        "All network telemetry features": list(set(all_telemetry_features)),
        "All telemetry + router topology": all_telemetry_plus_router
    }

    ablation_results = []
    print("\nRunning ablation experiments...")
    for group_name, feat_cols in subsets.items():
        print(f"--> Evaluating subset: {group_name} ({len(feat_cols)} features)...")
        prep = ResearchDataPreprocessor(feat_cols)
        X_train_sub = prep.fit_transform(train_df)
        X_val_sub = prep.transform(val_df)
        X_test_sub = prep.transform(test_df)

        model = lgb.LGBMClassifier(
            n_estimators=100, max_depth=6, class_weight="balanced",
            random_state=42, n_jobs=-1, verbose=-1
        )
        model.fit(X_train_sub, y_train)

        val_probs = model.predict_proba(X_val_sub)[:, 1]
        opt_thresh, _, _ = find_optimal_threshold(y_val, val_probs, metric="f1")

        test_probs = model.predict_proba(X_test_sub)[:, 1]
        m = calculate_metrics_at_threshold(y_test, test_probs, opt_thresh)

        ablation_results.append({
            "feature_group": group_name,
            "feature_count": len(feat_cols),
            "optimal_threshold": opt_thresh,
            "pr_auc": m["pr_auc"],
            "roc_auc": m["roc_auc"],
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "f2": m["f2"]
        })

    os.makedirs(artifacts_dir, exist_ok=True)
    out_path = os.path.join(artifacts_dir, "ablation_results.json")
    with open(out_path, "w") as f:
        json.dump(ablation_results, f, indent=2)

    print("Ablation study completed and saved.")
    return ablation_results

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    d_path = os.path.join(current_dir, "..", "data", "lcore_d_network_future_fault_30m.csv")
    art_path = os.path.join(current_dir, "artifacts")
    run_ablation_study(d_path, art_path)
