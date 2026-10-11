"""Network discovery and session REST endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database.session import get_db
from ..services.session_service import SessionService
from ..schemas.network_schemas import NetworkStatusResponse, NetworkSessionItem

router = APIRouter(prefix="/api/network", tags=["Network"])
session_service = SessionService()

@router.get("/status")
def get_network_status(db: Session = Depends(get_db)) -> Dict[str, Any]:
    from ..main import global_state
    latest = global_state.get("latest_telemetry") or {}
    return {
        "adapter_name": latest.get("adapter_name", "Unknown"),
        "connection_state": latest.get("connection_state", "unknown"),
        "ssid_hash": latest.get("ssid_hash"),
        "gateway_ip": latest.get("gateway_ip"),
        "local_ip": latest.get("local_ip"),
        "is_gateway_reachable": bool(latest.get("gateway_reachable")),
        "is_internet_reachable": bool(latest.get("internet_reachable")),
        "signal_percent": latest.get("signal_strength"),
        "channel": latest.get("wifi_channel"),
        "link_speed_mbps": latest.get("link_speed"),
        "session_id": latest.get("session_id")
    }

@router.get("/interfaces")
def get_network_interfaces() -> List[Dict[str, Any]]:
    import psutil
    stats = psutil.net_if_stats()
    interfaces = []
    for name, stat in stats.items():
        interfaces.append({
            "name": name,
            "is_up": stat.isup,
            "speed_mbps": stat.speed,
            "duplex": str(stat.duplex)
        })
    return interfaces

@router.get("/session")
def get_current_session(db: Session = Depends(get_db)) -> Dict[str, Any]:
    from ..main import global_state
    latest = global_state.get("latest_telemetry") or {}
    sess_id = latest.get("session_id")
    sessions = session_service.get_all_sessions(db)
    current = next((s for s in sessions if s["session_id"] == sess_id), None)
    return current or {"session_id": sess_id, "is_active": True}

@router.get("/sessions")
def get_all_sessions(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    return session_service.get_all_sessions(db)
