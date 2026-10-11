"""Telemetry REST endpoints."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database.session import get_db
from ..services.telemetry_service import TelemetryService
from ..schemas.telemetry_schemas import TelemetryHistoryResponse

router = APIRouter(prefix="/api/telemetry", tags=["Telemetry"])
telemetry_service = TelemetryService()

@router.get("/current")
def get_current_telemetry() -> Dict[str, Any]:
    from ..main import global_state
    latest = global_state.get("latest_telemetry")
    if not latest:
        return {"status": "NO_DATA_YET"}
    return latest

@router.get("/history")
def get_telemetry_history(
    timeframe: str = Query("1h", pattern="^(15m|1h|6h|24h|7d)$"),
    db: Session = Depends(get_db)
):
    points = telemetry_service.get_history(db, timeframe=timeframe)
    return {
        "timeframe": timeframe,
        "total_points": len(points),
        "data": points
    }
