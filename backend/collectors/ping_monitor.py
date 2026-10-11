"""
Dual-Path ICMP Ping Monitor for Local Gateway and External Internet.
Computes latency, packet loss, and jitter concurrently.
"""

import subprocess
import re
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional

class PingMonitor:
    def __init__(self, internet_target: str = "1.1.1.1", ping_count: int = 3, timeout_ms: int = 800):
        self.internet_target = internet_target
        self.ping_count = ping_count
        self.timeout_ms = timeout_ms

    def ping_target(self, host: Optional[str]) -> Dict[str, Any]:
        """Executes ICMP ping to target host and extracts latency, loss %, and jitter."""
        if not host:
            return {"latency": None, "packet_loss": 100.0, "jitter": 0.0, "target": None, "reachable": False}

        cmd = ["ping", "-n", str(self.ping_count), "-w", str(self.timeout_ms), host]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=(self.ping_count * self.timeout_ms / 1000.0) + 2.0)
            output = res.stdout

            # Parse replies
            # E.g. "Reply from 1.1.1.1: bytes=32 time=24ms TTL=58" or "Request timed out."
            rtt_times = []
            for line in output.splitlines():
                if "time=" in line or "time<" in line:
                    m = re.search(r"time[<=](\d+)ms", line)
                    if m:
                        rtt_times.append(float(m.group(1)))

            sent = self.ping_count
            received = len(rtt_times)
            loss_pct = round(((sent - received) / sent) * 100.0, 1)

            if rtt_times:
                mean_rtt = round(float(np.mean(rtt_times)), 2)
                jitter = round(float(np.std(rtt_times)), 2) if len(rtt_times) > 1 else 0.0
                return {
                    "latency": mean_rtt,
                    "packet_loss": loss_pct,
                    "jitter": jitter,
                    "target": host,
                    "reachable": True
                }
            else:
                return {
                    "latency": None,
                    "packet_loss": 100.0,
                    "jitter": 0.0,
                    "target": host,
                    "reachable": False
                }
        except Exception:
            return {
                "latency": None,
                "packet_loss": 100.0,
                "jitter": 0.0,
                "target": host,
                "reachable": False
            }

    def measure_dual_paths(self, gateway_ip: Optional[str]) -> Dict[str, Any]:
        """Concurrently measures Local Gateway path and External Internet path."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            fut_gw = executor.submit(self.ping_target, gateway_ip)
            fut_inet = executor.submit(self.ping_target, self.internet_target)

            gw_res = fut_gw.result()
            inet_res = fut_inet.result()

        return {
            "gateway_latency": gw_res["latency"],
            "gateway_packet_loss": gw_res["packet_loss"],
            "gateway_jitter": gw_res["jitter"],
            "gateway_reachable": gw_res["reachable"],
            "internet_latency": inet_res["latency"],
            "internet_packet_loss": inet_res["packet_loss"],
            "internet_jitter": inet_res["jitter"],
            "internet_reachable": inet_res["reachable"],
            "gateway_target": gateway_ip,
            "internet_target": self.internet_target
        }

if __name__ == "__main__":
    monitor = PingMonitor()
    # Test with 1.1.1.1 as external and fallback
    print("Dual Path Ping:", monitor.measure_dual_paths("172.17.238.131"))
