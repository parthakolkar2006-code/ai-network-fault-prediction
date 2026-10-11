from pydantic import BaseModel
from typing import Optional, List

class NetworkStatusResponse(BaseModel):
    adapter_name: Optional[str] = None
    connection_state: str
    ssid_hash: Optional[str] = None
    gateway_ip: Optional[str] = None
    local_ip: Optional[str] = None
    is_gateway_reachable: bool = False
    is_internet_reachable: bool = False
    signal_percent: Optional[int] = None
    channel: Optional[int] = None
    link_speed_mbps: Optional[float] = None
    session_id: Optional[str] = None

class NetworkInterfaceItem(BaseModel):
    name: str
    is_up: bool
    speed_mbps: Optional[int] = None
    duplex: Optional[str] = None

class NetworkSessionItem(BaseModel):
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    ssid_hash: Optional[str] = None
    gateway_ip: Optional[str] = None
    local_ip: Optional[str] = None
    interface_name: Optional[str] = None
    duration_seconds: Optional[int] = None
    avg_gateway_latency: Optional[float] = None
    avg_gateway_loss: Optional[float] = None
    peak_risk: Optional[float] = None
    is_active: bool = False
