"""Network Session service for tracking Wi-Fi networks and gateway transitions."""
import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.db_models import NetworkSession, TelemetryRecord, PredictionRecord

class SessionService:
    def sync_session(
        self,
        db: Session,
        session_id: str,
        ssid_hash: Optional[str],
        gateway_ip: Optional[str],
        local_ip: Optional[str],
        interface_name: Optional[str]
    ) -> NetworkSession:
        """Ensures the active session exists in DB, deactivates older sessions if changed."""
        sess = db.query(NetworkSession).filter(NetworkSession.session_id == session_id).first()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not sess:
            # Close existing active sessions
            db.query(NetworkSession).filter(NetworkSession.is_active == True).update({
                "is_active": False,
                "end_time": now_str
            })
            sess = NetworkSession(
                session_id=session_id,
                start_time=now_str,
                ssid_hash=ssid_hash,
                gateway_ip=gateway_ip,
                local_ip=local_ip,
                interface_name=interface_name,
                is_active=True
            )
            db.add(sess)
            db.commit()
            db.refresh(sess)
        return sess

    def get_all_sessions(self, db: Session) -> List[Dict[str, Any]]:
        """Retrieves all sessions with aggregated average latency, loss, and peak risk."""
        sessions = db.query(NetworkSession).order_by(NetworkSession.id.desc()).all()
        results = []

        for s in sessions:
            # Aggregates from telemetry
            stats = db.query(
                func.avg(TelemetryRecord.gateway_latency).label("avg_lat"),
                func.avg(TelemetryRecord.gateway_packet_loss).label("avg_loss")
            ).filter(TelemetryRecord.session_id == s.session_id).first()

            # Peak risk from predictions
            peak_pred = db.query(func.max(PredictionRecord.risk_probability)).filter(
                PredictionRecord.session_id == s.session_id
            ).scalar()

            avg_lat = round(float(stats.avg_lat), 2) if stats and stats.avg_lat is not None else None
            avg_loss = round(float(stats.avg_loss), 2) if stats and stats.avg_loss is not None else None
            peak_risk = round(float(peak_pred), 3) if peak_pred is not None else None

            # Duration calculation
            duration_sec = None
            try:
                start_dt = datetime.datetime.strptime(s.start_time, "%Y-%m-%d %H:%M:%S")
                end_dt = datetime.datetime.strptime(s.end_time, "%Y-%m-%d %H:%M:%S") if s.end_time else datetime.datetime.now()
                duration_sec = int((end_dt - start_dt).total_seconds())
            except Exception:
                pass

            results.append({
                "session_id": s.session_id,
                "start_time": s.start_time,
                "end_time": s.end_time,
                "ssid_hash": s.ssid_hash or "N/A",
                "gateway_ip": s.gateway_ip or "N/A",
                "local_ip": s.local_ip or "N/A",
                "interface_name": s.interface_name or "N/A",
                "duration_seconds": duration_sec,
                "avg_gateway_latency": avg_lat,
                "avg_gateway_loss": avg_loss,
                "peak_risk": peak_risk,
                "is_active": s.is_active
            })

        return results
