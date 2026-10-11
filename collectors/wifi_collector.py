"""
Windows Wi-Fi telemetry collector using netsh wlan.
Extracts SSID, BSSID, RSSI, Signal %, Channel, Tx/Rx rates.
Hashes SSID for privacy compliance.
"""

import subprocess
import hashlib
import re
from typing import Dict, Any, Optional

class WiFiCollector:
    def __init__(self):
        pass

    def get_wifi_telemetry(self) -> Dict[str, Any]:
        """Collects live Wi-Fi telemetry from Windows netsh wlan."""
        try:
            res = subprocess.run(
                ["netsh", "wlan", "show", "interfaces"],
                capture_output=True, text=True, timeout=3
            )
            if res.returncode != 0 or not res.stdout:
                return self._empty_response("Disconnected or netsh error")
            return self._parse_netsh_output(res.stdout)
        except Exception as e:
            return self._empty_response(str(e))

    def _parse_netsh_output(self, output: str) -> Dict[str, Any]:
        data = {
            "adapter_name": None,
            "connection_state": "disconnected",
            "ssid": None,
            "ssid_hash": None,
            "bssid": None,
            "channel": None,
            "signal_percent": None,
            "rssi_dbm": None,
            "rx_rate_mbps": None,
            "tx_rate_mbps": None,
            "radio_type": None,
            "authentication": None
        }

        for line in output.splitlines():
            line = line.strip()
            if not line or ":" not in line:
                continue
            key, val = [p.strip() for p in line.split(":", 1)]

            if key == "Name":
                data["adapter_name"] = val
            elif key == "State":
                data["connection_state"] = val.lower()
            elif key == "SSID":
                data["ssid"] = val
                data["ssid_hash"] = hashlib.sha256(val.encode()).hexdigest()[:12] if val else None
            elif key == "AP BSSID" or key == "BSSID":
                data["bssid"] = val
            elif key == "Channel":
                try:
                    data["channel"] = int(val)
                except ValueError:
                    data["channel"] = None
            elif key == "Signal":
                # E.g. "98%"
                m = re.search(r"(\d+)", val)
                if m:
                    data["signal_percent"] = int(m.group(1))
            elif key == "Rssi":
                # E.g. "-42"
                try:
                    data["rssi_dbm"] = int(val)
                except ValueError:
                    data["rssi_dbm"] = None
            elif key == "Receive rate (Mbps)":
                try:
                    data["rx_rate_mbps"] = float(val)
                except ValueError:
                    data["rx_rate_mbps"] = None
            elif key == "Transmit rate (Mbps)":
                try:
                    data["tx_rate_mbps"] = float(val)
                except ValueError:
                    data["tx_rate_mbps"] = None
            elif key == "Radio type":
                data["radio_type"] = val
            elif key == "Authentication":
                data["authentication"] = val

        return data

    def _empty_response(self, reason: str) -> Dict[str, Any]:
        return {
            "adapter_name": None,
            "connection_state": "disconnected",
            "ssid": None,
            "ssid_hash": None,
            "bssid": None,
            "channel": None,
            "signal_percent": None,
            "rssi_dbm": None,
            "rx_rate_mbps": None,
            "tx_rate_mbps": None,
            "radio_type": None,
            "authentication": None,
            "error_detail": reason
        }

if __name__ == "__main__":
    collector = WiFiCollector()
    print("WiFi Telemetry:", collector.get_wifi_telemetry())
