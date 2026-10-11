"""Alerts query endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database.session import get_db
from ..services.alert_service import AlertService

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])
alert_service = AlertService()

@router.get("")
def get_alerts(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    return alert_service.get_recent_alerts(db, limit=50)
