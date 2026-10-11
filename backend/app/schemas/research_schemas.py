from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ModelComparisonEntry(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_name: str
    optimal_threshold: float
    test_roc_auc: float
    test_pr_auc: float
    test_precision: float
    test_recall: float
    test_f1: float
    test_f2: float
    test_specificity: float
    test_fpr: float
    test_fnr: float
    confusion_matrix: Dict[str, int]

class CurvePoint(BaseModel):
    x: float
    y: float

class ModelCurves(BaseModel):
    roc_curve: List[CurvePoint]
    pr_curve: List[CurvePoint]

class FeatureImportanceItem(BaseModel):
    feature: str
    importance: float

class AblationItem(BaseModel):
    feature_group: str
    feature_count: int
    optimal_threshold: float
    pr_auc: float
    roc_auc: float
    precision: float
    recall: float
    f1: float
    f2: float

class DatasetInfoResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    source: str
    model_rows: int
    positive_rows: int
    negative_rows: int
    positive_rate: float
    fault_events: int
    time_start: str
    time_end: str
    feature_count: int
    features: List[str]
    split_info: Optional[Dict[str, Any]] = None
