from pydantic import BaseModel
from typing import Optional, List, Any, Dict

class ContributingFactor(BaseModel):
    feature: str
    impact: float
    value: Any
    direction: str

class PredictionCurrentResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    timestamp: str
    session_id: str
    is_model_trained: bool
    status: str
    message: str
    risk_probability: Optional[float] = None
    prediction_state: str  # NORMAL, WATCH, ELEVATED, HIGH RISK, BASELINE_COLLECTION
    threshold: Optional[float] = None
    model_version: str
    network_health_indicator: Optional[str] = "STABLE"
    contributing_factors: List[ContributingFactor] = []

class PredictionHistoryPoint(BaseModel):
    timestamp: str
    risk_probability: Optional[float] = None
    prediction_state: str
    network_instability_score: Optional[float] = None

class PredictionHistoryResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_version: str
    total_points: int
    data: List[PredictionHistoryPoint]

class SimulationRequest(BaseModel):
    scenario: str = "moderate"
    custom_overrides: Optional[Dict[str, Any]] = None

class SimulationResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    scenario: str
    model_name: str
    risk_probability: float
    threshold: float
    prediction_state: str
    contributing_factors: List[ContributingFactor] = []
    key_metrics_summary: Dict[str, Any]
    raw_features_count: Optional[int] = 79

