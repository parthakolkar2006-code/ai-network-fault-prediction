"""Telemetry storage, buffer management, and history retrieval service."""
import datetime
import pandas as pd
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from ..models.db_models import TelemetryRecord

class TelemetryService:
    def __init__(self, max_buffer_size: int = 1200):
        self.max_buffer_size = max_buffer_size
        self._memory_buffer: List[Dict[str, Any]] = []

    def save_telemetry(self, db: Session, telemetry_data: Dict[str, Any]) -> TelemetryRecord:
        """Stores telemetry into DB and in-memory buffer."""
        # Add to buffer
        self._memory_buffer.append(telemetry_data)
        if len(self._memory_buffer) > self.max_buffer_size:
            self._memory_buffer.pop(0)

        record = TelemetryRecord(
            timestamp=telemetry_data["timestamp"],
            session_id=telemetry_data["session_id"],
            gateway_latency=telemetry_data.get("gateway_latency"),
            gateway_packet_loss=telemetry_data.get("gateway_packet_loss"),
            gateway_jitter=telemetry_data.get("gateway_jitter"),
            internet_latency=telemetry_data.get("internet_latency"),
            internet_packet_loss=telemetry_data.get("internet_packet_loss"),
            internet_jitter=telemetry_data.get("internet_jitter"),
            signal_strength=telemetry_data.get("signal_strength"),
            link_speed=telemetry_data.get("link_speed"),
            wifi_channel=telemetry_data.get("wifi_channel"),
            download_bps=telemetry_data.get("download_bps", 0),
            upload_bps=telemetry_data.get("upload_bps", 0),
            packet_errors=telemetry_data.get("packet_errors", 0),
            packet_discards=telemetry_data.get("packet_discards", 0),
            interface_status=telemetry_data.get("interface_status", "UP"),
            network_disconnect_event=telemetry_data.get("network_disconnect_event", 0)
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def get_recent_dataframe(self) -> pd.DataFrame:
        """Returns in-memory buffer as pandas DataFrame for feature extraction."""
        if not self._memory_buffer:
            return pd.DataFrame()
        return pd.DataFrame(self._memory_buffer)

    def get_history(self, db: Session, timeframe: str = "1h") -> List[Dict[str, Any]]:
        """Queries telemetry records within a given timeframe."""
        delta_map = {
            "15m": datetime.timedelta(minutes=15),
            "1h": datetime.timedelta(hours=1),
            "6h": datetime.timedelta(hours=6),
            "24h": datetime.timedelta(hours=24),
            "7d": datetime.timedelta(days=7)
        }
        cutoff_delta = delta_map.get(timeframe, datetime.timedelta(hours=1))
        cutoff_dt = datetime.datetime.now() - cutoff_delta
        cutoff_str = cutoff_dt.strftime("%Y-%m-%d %H:%M:%S")

        records = db.query(TelemetryRecord).filter(
            TelemetryRecord.timestamp >= cutoff_str
        ).order_by(TelemetryRecord.id.asc()).all()

        results = []
        for r in records:
            results.append({
                "timestamp": r.timestamp,
                "session_id": r.session_id,
                "gateway_latency": r.gateway_latency,
                "gateway_packet_loss": r.gateway_packet_loss,
                "gateway_jitter": r.gateway_jitter,
                "gateway_reachable": r.gateway_latency is not None,
                "internet_latency": r.internet_latency,
                "internet_packet_loss": r.internet_packet_loss,
                "internet_jitter": r.internet_jitter,
                "internet_reachable": r.internet_latency is not None,
                "signal_strength": r.signal_strength,
                "link_speed": r.link_speed,
                "wifi_channel": r.wifi_channel,
                "download_bps": r.download_bps,
                "upload_bps": r.upload_bps,
                "download_mbps": round(r.download_bps / 1_000_000, 2),
                "upload_mbps": round(r.upload_bps / 1_000_000, 2),
                "packet_errors": r.packet_errors,
                "packet_discards": r.packet_discards,
                "interface_status": r.interface_status,
                "network_disconnect_event": r.network_disconnect_event
            })
        return results
