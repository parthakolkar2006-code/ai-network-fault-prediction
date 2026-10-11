"""SQLAlchemy database models for sessions, telemetry, predictions, alerts, and model versions."""
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Text, Index
from ..database.base import Base

class NetworkSession(Base):
    __tablename__ = "network_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(64), unique=True, index=True, nullable=False)
    start_time = Column(String(32), nullable=False)
    end_time = Column(String(32), nullable=True)
    ssid_hash = Column(String(64), nullable=True)
    gateway_ip = Column(String(64), nullable=True)
    local_ip = Column(String(64), nullable=True)
    interface_name = Column(String(64), nullable=True)
    is_active = Column(Boolean, default=True)

class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String(32), index=True, nullable=False)
    session_id = Column(String(64), index=True, nullable=False)
    gateway_latency = Column(Float, nullable=True)
    gateway_packet_loss = Column(Float, nullable=True)
    gateway_jitter = Column(Float, nullable=True)
    internet_latency = Column(Float, nullable=True)
    internet_packet_loss = Column(Float, nullable=True)
    internet_jitter = Column(Float, nullable=True)
    signal_strength = Column(Float, nullable=True)
    link_speed = Column(Float, nullable=True)
    wifi_channel = Column(Integer, nullable=True)
    download_bps = Column(Integer, default=0)
    upload_bps = Column(Integer, default=0)
    packet_errors = Column(Integer, default=0)
    packet_discards = Column(Integer, default=0)
    interface_status = Column(String(16), default="UP")
    network_disconnect_event = Column(Integer, default=0)

    __table_args__ = (
        Index("idx_telemetry_session_time", "session_id", "timestamp"),
    )

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String(32), index=True, nullable=False)
    session_id = Column(String(64), index=True, nullable=False)
    model_version = Column(String(64), nullable=False)
    risk_probability = Column(Float, nullable=True)
    prediction_state = Column(String(32), nullable=False)
    threshold = Column(Float, nullable=True)
    explanation_json = Column(Text, nullable=True)

class AlertRecord(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String(32), index=True, nullable=False)
    session_id = Column(String(64), nullable=True)
    severity = Column(String(16), nullable=False)  # INFO, WARNING, HIGH, CRITICAL
    message = Column(String(256), nullable=False)
    status = Column(String(16), default="ACTIVE")   # ACTIVE, RESOLVED

class ModelVersionRecord(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String(64), unique=True, index=True, nullable=False)
    model_type = Column(String(32), nullable=False)  # RESEARCH_BENCHMARK, WIFI_DEPLOYMENT
    version = Column(String(32), nullable=False)
    created_at = Column(String(32), nullable=False)
    metrics_json = Column(Text, nullable=True)
    threshold = Column(Float, nullable=True)
