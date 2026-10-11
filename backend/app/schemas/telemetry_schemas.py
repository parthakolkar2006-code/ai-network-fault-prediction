from pydantic import BaseModel
from typing import Optional, List, Any

class TelemetrySnapshot(BaseModel):
    timestamp: str
    session_id: str
    ssid_hash: Optional[str] = None
    gateway_ip: Optional[str] = None
    local_ip: Optional[str] = None
    adapter_name: Optional[str] = None
    connection_state: Optional[str] = None
    gateway_latency: Optional[float] = None
    gateway_packet_loss: Optional[float] = None
    gateway_jitter: Optional[float] = None
    gateway_reachable: bool = False
    internet_latency: Optional[float] = None
    internet_packet_loss: Optional[float] = None
    internet_jitter: Optional[float] = None
    internet_reachable: bool = False
    signal_strength: Optional[float] = None
    rssi_dbm: Optional[int] = None
    wifi_channel: Optional[int] = None
    link_speed: Optional[float] = None
    download_bps: int = 0
    upload_bps: int = 0
    download_mbps: float = 0.0
    upload_mbps: float = 0.0
    packet_errors: int = 0
    packet_discards: int = 0
    interface_status: str = "UP"
    network_disconnect_event: int = 0

class TelemetryHistoryResponse(BaseModel):
    timeframe: str
    total_points: int
    data: List[TelemetrySnapshot]
