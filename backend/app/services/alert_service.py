"""Alert service with debounce and cooldown mechanisms to prevent alert fatigue."""
import time
import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..models.db_models import AlertRecord

class AlertService:
    def __init__(self, cooldown_seconds: int = 60):
        self.cooldown_seconds = cooldown_seconds
        self.last_alert_time: Dict[str, float] = {}

    def check_and_generate_alerts(
        self,
        db: Session,
        telemetry: Dict[str, Any],
        prediction: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Evaluates alerts with cooldown to suppress duplicate flooding."""
        now_ts = time.time()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_id = telemetry.get("session_id")
        created_alerts = []

        def should_fire(key: str) -> bool:
            last = self.last_alert_time.get(key, 0)
            if now_ts - last > self.cooldown_seconds:
                self.last_alert_time[key] = now_ts
                return True
            return False

        # Condition 1: High packet loss
        gw_loss = telemetry.get("gateway_packet_loss") or 0.0
        inet_loss = telemetry.get("internet_packet_loss") or 0.0
        if gw_loss >= 50.0 and should_fire("gw_loss_critical"):
            created_alerts.append(self._save_alert(db, now_str, session_id, "CRITICAL", f"Local Gateway experiencing {gw_loss}% packet loss"))
        elif inet_loss >= 50.0 and should_fire("inet_loss_critical"):
            created_alerts.append(self._save_alert(db, now_str, session_id, "HIGH", f"Internet path experiencing {inet_loss}% packet loss"))

        # Condition 2: Network disconnection
        if telemetry.get("network_disconnect_event") == 1 and should_fire("disconnect_event"):
            created_alerts.append(self._save_alert(db, now_str, session_id, "WARNING", "Network disconnection or transition detected"))

        # Condition 3: Prediction state elevated / high risk
        pred_state = prediction.get("prediction_state")
        if pred_state == "HIGH RISK" and should_fire("pred_high_risk"):
            created_alerts.append(self._save_alert(db, now_str, session_id, "HIGH", "AI predicts severe network degradation within 30 minutes"))
        elif pred_state == "ELEVATED" and should_fire("pred_elevated"):
            created_alerts.append(self._save_alert(db, now_str, session_id, "WARNING", "AI predicts elevated risk of network fault within 30 minutes"))

        return created_alerts

    def _save_alert(self, db: Session, timestamp: str, session_id: Optional[str], severity: str, message: str) -> Dict[str, Any]:
        alert = AlertRecord(
            timestamp=timestamp,
            session_id=session_id,
            severity=severity,
            message=message,
            status="ACTIVE"
        )
        db.add(alert)
        db.commit()
        return {
            "timestamp": timestamp,
            "severity": severity,
            "message": message,
            "status": "ACTIVE"
        }

    def get_recent_alerts(self, db: Session, limit: int = 50) -> List[Dict[str, Any]]:
        alerts = db.query(AlertRecord).order_by(AlertRecord.id.desc()).limit(limit).all()
        return [{
            "id": a.id,
            "timestamp": a.timestamp,
            "severity": a.severity,
            "message": a.message,
            "status": a.status
        } for a in alerts]
