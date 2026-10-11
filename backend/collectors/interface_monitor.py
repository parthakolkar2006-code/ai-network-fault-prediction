"""
Network interface traffic and error monitor using psutil.
Calculates download_bps, upload_bps, errors, and discards.
"""

import time
import psutil
from typing import Dict, Any, Optional

class InterfaceMonitor:
    def __init__(self):
        self.last_time = time.time()
        self.last_io = psutil.net_io_counters()

    def get_interface_metrics(self) -> Dict[str, Any]:
        """Calculates instantaneous bandwidth and error metrics across network interfaces."""
        now = time.time()
        current_io = psutil.net_io_counters()
        dt = max(0.1, now - self.last_time)

        bytes_recv_delta = max(0, current_io.bytes_recv - self.last_io.bytes_recv)
        bytes_sent_delta = max(0, current_io.bytes_sent - self.last_io.bytes_sent)

        # bits per second
        download_bps = int((bytes_recv_delta * 8) / dt)
        upload_bps = int((bytes_sent_delta * 8) / dt)

        # errors and discards
        packet_errors = (current_io.errin + current_io.errout)
        packet_discards = (current_io.dropin + current_io.dropout)

        self.last_time = now
        self.last_io = current_io

        # Find status of primary wireless / active interfaces
        stats = psutil.net_if_stats()
        active_interfaces = []
        for name, stat in stats.items():
            if stat.isup:
                active_interfaces.append({
                    "name": name,
                    "is_up": stat.isup,
                    "speed_mbps": stat.speed,
                    "duplex": str(stat.duplex)
                })

        return {
            "download_bps": download_bps,
            "upload_bps": upload_bps,
            "download_mbps": round(download_bps / 1_000_000, 2),
            "upload_mbps": round(upload_bps / 1_000_000, 2),
            "packet_errors": packet_errors,
            "packet_discards": packet_discards,
            "active_interfaces": active_interfaces,
            "interface_status": "UP" if len(active_interfaces) > 0 else "DOWN"
        }

if __name__ == "__main__":
    monitor = InterfaceMonitor()
    time.sleep(1.0)
    print("Interface Metrics:", monitor.get_interface_metrics())
