"""
Network Discovery & Telemetry Coordinator.
Manages network session lifecycle across Wi-Fi networks (Home, College, Hotspot).
"""

import time
import uuid
import datetime
from typing import Dict, Any, Optional, Tuple

from .gateway_detector import GatewayDetector
from .wifi_collector import WiFiCollector
from .ping_monitor import PingMonitor
from .interface_monitor import InterfaceMonitor

class NetworkDiscovery:
    def __init__(self, ping_target_internet: str = "1.1.1.1"):
        self.gateway_detector = GatewayDetector()
        self.wifi_collector = WiFiCollector()
        self.ping_monitor = PingMonitor(internet_target=ping_target_internet)
        self.interface_monitor = InterfaceMonitor()

        self.current_session_id: Optional[str] = None
        self.current_ssid_hash: Optional[str] = None
        self.current_gateway_ip: Optional[str] = None
        self.session_start_time: Optional[str] = None

    def _ensure_session(self, ssid_hash: Optional[str], gateway_ip: Optional[str], local_ip: Optional[str], interface_name: Optional[str]) -> Tuple[str, bool]:
        """Creates or rotates network session when network or gateway changes."""
        has_changed = False
        now_iso = datetime.datetime.now().isoformat()

        if (self.current_session_id is None or
            ssid_hash != self.current_ssid_hash or
            gateway_ip != self.current_gateway_ip):
            
            has_changed = True
            new_id = f"sess_{int(time.time())}_{uuid.uuid4().hex[:6]}"
            self.current_session_id = new_id
            self.current_ssid_hash = ssid_hash
            self.current_gateway_ip = gateway_ip
            self.session_start_time = now_iso

        return self.current_session_id, has_changed

    def collect_live_snapshot(self) -> Dict[str, Any]:
        """Collects a complete synchronous telemetry snapshot across all collectors."""
        now_dt = datetime.datetime.now()
        timestamp_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")

        # 1. Gateway & Local IP
        gw_info = self.gateway_detector.get_default_gateway()
        gateway_ip = gw_info.get("gateway_ip")
        local_ip = gw_info.get("local_ip")
        detected_iface = gw_info.get("interface_name")

        # 2. Wi-Fi telemetry
        wifi_info = self.wifi_collector.get_wifi_telemetry()
        ssid_hash = wifi_info.get("ssid_hash")
        adapter_name = wifi_info.get("adapter_name") or detected_iface or "Wi-Fi"

        # 3. Session lifecycle
        from typing import Tuple
        session_id, network_changed = self._ensure_session(ssid_hash, gateway_ip, local_ip, adapter_name)

        # 4. Dual-Path Ping
        ping_info = self.ping_monitor.measure_dual_paths(gateway_ip)

        # 5. Interface bandwidth & errors
        iface_info = self.interface_monitor.get_interface_metrics()

        # Check disconnect state
        is_disconnected = (wifi_info.get("connection_state") == "disconnected") or (gateway_ip is None and not ping_info["internet_reachable"])

        telemetry = {
            "timestamp": timestamp_str,
            "session_id": session_id,
            "ssid_hash": ssid_hash or "unidentified",
            "gateway_ip": gateway_ip or "unassigned",
            "local_ip": local_ip or "127.0.0.1",
            "adapter_name": adapter_name,
            "connection_state": wifi_info.get("connection_state", "connected"),
            # Local gateway health
            "gateway_latency": ping_info["gateway_latency"],
            "gateway_packet_loss": ping_info["gateway_packet_loss"],
            "gateway_jitter": ping_info["gateway_jitter"],
            "gateway_reachable": ping_info["gateway_reachable"],
            # Internet health
            "internet_latency": ping_info["internet_latency"],
            "internet_packet_loss": ping_info["internet_packet_loss"],
            "internet_jitter": ping_info["internet_jitter"],
            "internet_reachable": ping_info["internet_reachable"],
            # Wi-Fi parameters
            "signal_strength": wifi_info.get("signal_percent"),
            "rssi_dbm": wifi_info.get("rssi_dbm"),
            "wifi_channel": wifi_info.get("channel"),
            "link_speed": wifi_info.get("rx_rate_mbps"),
            "tx_rate_mbps": wifi_info.get("tx_rate_mbps"),
            "radio_type": wifi_info.get("radio_type"),
            # Traffic
            "download_bps": iface_info["download_bps"],
            "upload_bps": iface_info["upload_bps"],
            "download_mbps": iface_info["download_mbps"],
            "upload_mbps": iface_info["upload_mbps"],
            "packet_errors": iface_info["packet_errors"],
            "packet_discards": iface_info["packet_discards"],
            "interface_status": iface_info["interface_status"],
            # Events
            "network_disconnect_event": 1 if is_disconnected or network_changed else 0,
            "network_changed": network_changed
        }

        return telemetry

if __name__ == "__main__":
    discovery = NetworkDiscovery()
    import json
    print(json.dumps(discovery.collect_live_snapshot(), indent=2))
