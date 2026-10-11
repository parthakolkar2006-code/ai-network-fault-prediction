"""
Research-grade evaluation metrics and curve generation.
All calculations are strictly computed from actual predictions and ground truth.
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from sklearn.metrics import (
    roc_auc_score, average_precision_score, confusion_matrix,
    roc_curve, precision_recall_curve
)

def calculate_metrics_at_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    threshold: float
) -> Dict[str, Any]:
    """Calculates full confusion matrix and classification metrics at a locked threshold."""
    y_pred = (y_prob >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    
    total = len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0.0
    
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    f2 = (1 + 2**2) * (precision * recall) / ((2**2 * precision) + recall) if ((4 * precision) + recall) > 0 else 0.0
    accuracy = (tp + tn) / total if total > 0 else 0.0
    
    roc_auc = float(roc_auc_score(y_true, y_prob)) if len(np.unique(y_true)) > 1 else 0.5
    pr_auc = float(average_precision_score(y_true, y_prob)) if len(np.unique(y_true)) > 1 else 0.0

    return {
        "threshold": round(float(threshold), 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision), 4),
        "recall": round(float(recall), 4),
        "f1": round(float(f1), 4),
        "f2": round(float(f2), 4),
        "specificity": round(float(specificity), 4),
        "false_positive_rate": round(float(fpr), 4),
        "false_negative_rate": round(float(fnr), 4),
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "tn": int(tn),
        "total_samples": int(total),
        "positive_samples": int(tp + fn),
        "negative_samples": int(tn + fp)
    }

def find_optimal_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    metric: str = "f1"
) -> Tuple[float, Dict[str, Any], List[Dict[str, Any]]]:
    """
    Sweeps thresholds on validation set to find the optimal decision boundary.
    Returns optimal threshold, metrics at that threshold, and threshold curve data.
    """
    thresholds = np.linspace(0.01, 0.99, 99)
    best_thresh = 0.5
    best_score = -1.0
    best_metrics = {}
    curve_data = []

    for t in thresholds:
        m = calculate_metrics_at_threshold(y_true, y_prob, float(t))
        score = m.get(metric, 0.0)
        curve_data.append({
            "threshold": round(float(t), 2),
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "f2": m["f2"],
            "fpr": m["false_positive_rate"]
        })
        if score > best_score:
            best_score = score
            best_thresh = float(t)
            best_metrics = m

    return best_thresh, best_metrics, curve_data

def generate_curve_points(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    max_points: int = 50
) -> Dict[str, Any]:
    """Generates downsampled ROC and PR curves suitable for interactive frontend charts."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    precision, recall, _ = precision_recall_curve(y_true, y_prob)

    # Downsample evenly
    def downsample(x_arr, y_arr, n):
        if len(x_arr) <= n:
            return [{"x": round(float(x), 4), "y": round(float(y), 4)} for x, y in zip(x_arr, y_arr)]
        idx = np.linspace(0, len(x_arr) - 1, n, dtype=int)
        return [{"x": round(float(x_arr[i]), 4), "y": round(float(y_arr[i]), 4)} for i in idx]

    return {
        "roc_curve": downsample(fpr, tpr, max_points),
        "pr_curve": downsample(recall, precision, max_points)
    }
