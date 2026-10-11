"""
Dynamic Default Gateway Detector for Windows.
Never hardcodes any gateway IP. Detects network changes across Home, College, Hotspot, etc.
"""

import subprocess
import re
import socket
from typing import Optional, Dict, Any

class GatewayDetector:
    def __init__(self):
        self.last_gateway = None
        self.last_interface = None

    def get_default_gateway(self) -> Dict[str, Optional[str]]:
        """
        Dynamically discovers the current default gateway and local IP on Windows.
        Tries PowerShell Get-NetRoute, fallback to route print, fallback to ipconfig.
        """
        result = self._try_powershell_netroute()
        if not result.get("gateway_ip"):
            result = self._try_route_print()
        if not result.get("gateway_ip"):
            result = self._try_ipconfig()
        if not result.get("local_ip"):
            result["local_ip"] = self._get_local_ip_fallback(result.get("gateway_ip"))

        gw = result.get("gateway_ip")
        iface = result.get("interface_name")
        has_changed = (gw != self.last_gateway) or (iface != self.last_interface)
        self.last_gateway = gw
        self.last_interface = iface

        result["has_changed"] = has_changed
        return result

    def _try_powershell_netroute(self) -> Dict[str, Optional[str]]:
        try:
            cmd = [
                "powershell", "-NoProfile", "-Command",
                "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Select-Object -First 1 -Property InterfaceAlias, NextHop | ConvertTo-Json"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=4)
            if res.returncode == 0 and res.stdout.strip():
                import json
                data = json.loads(res.stdout)
                nh = data.get("NextHop")
                alias = data.get("InterfaceAlias")
                if nh and nh != "0.0.0.0":
                    return {"gateway_ip": str(nh).strip(), "interface_name": str(alias).strip()}
        except Exception:
            pass
        return {"gateway_ip": None, "interface_name": None}

    def _try_route_print(self) -> Dict[str, Optional[str]]:
        try:
            res = subprocess.run(["route", "print", "0.0.0.0"], capture_output=True, text=True, timeout=4)
            if res.returncode == 0:
                # Look for lines with 0.0.0.0 0.0.0.0 <gateway> <interface>
                for line in res.stdout.splitlines():
                    parts = line.strip().split()
                    if len(parts) >= 4 and parts[0] == "0.0.0.0" and parts[1] == "0.0.0.0":
                        gw = parts[2]
                        local_ip = parts[3]
                        if gw != "On-link" and re.match(r"^\d+\.\d+\.\d+\.\d+$", gw):
                            return {"gateway_ip": gw, "local_ip": local_ip, "interface_name": None}
        except Exception:
            pass
        return {"gateway_ip": None, "local_ip": None, "interface_name": None}

    def _try_ipconfig(self) -> Dict[str, Optional[str]]:
        try:
            res = subprocess.run(["ipconfig"], capture_output=True, text=True, timeout=4)
            if res.returncode == 0:
                current_adapter = None
                gw = None
                ipv4 = None
                for line in res.stdout.splitlines():
                    if "adapter" in line.lower():
                        current_adapter = line.strip().rstrip(":")
                    if "IPv4 Address" in line or "IPv4" in line:
                        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                        if m:
                            ipv4 = m.group(1)
                    if "Default Gateway" in line:
                        m = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                        if m:
                            gw = m.group(1)
                            if gw and gw != "0.0.0.0":
                                return {"gateway_ip": gw, "local_ip": ipv4, "interface_name": current_adapter}
        except Exception:
            pass
        return {"gateway_ip": None, "local_ip": None, "interface_name": None}

    def _get_local_ip_fallback(self, gateway_ip: Optional[str]) -> Optional[str]:
        if not gateway_ip:
            target = "1.1.1.1"
        else:
            target = gateway_ip
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(1.0)
            s.connect((target, 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

if __name__ == "__main__":
    detector = GatewayDetector()
    info = detector.get_default_gateway()
    print("Gateway Detection Output:", info)
