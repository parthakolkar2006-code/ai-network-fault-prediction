# System Architecture Blueprint

## 1. Architectural Overview

The system implements a dual-engine architecture to address domain-shift separation between core ISP network benchmarking and real laptop Wi-Fi edge monitoring:

```
+-----------------------------------------------------------------------------------+
|                           REACT DASHBOARD (PORT 5173)                             |
|  Overview | Live Monitoring | AI Prediction | History | Sessions | Dataset | Research |
+-----------------------------------------------------------------------------------+
                                         ^
                                         | REST & WebSockets (/ws/live)
                                         v
+-----------------------------------------------------------------------------------+
|                            FASTAPI BACKEND (PORT 8000)                            |
|  +-------------------------------------+  +------------------------------------+  |
|  |           REST API Routers          |  |         WebSocket Manager          |  |
|  |  /api/network      /api/telemetry   |  |  /ws/live (2s tick broadcast)      |  |
|  |  /api/prediction   /api/model       |  +------------------------------------+  |
|  |  /api/dataset      /api/research    |                                          |
|  +-------------------------------------+                                          |
|                                                                                   |
|  +-------------------------------------+  +------------------------------------+  |
|  |         Service Layer & ORM         |  |         Inference Pipeline         |  |
|  |  SessionService   TelemetryService  |  |  Research Engine (HistGB/LR/RF)    |  |
|  |  PredictionService AlertService     |  |  Deployment Engine (Baseline cold) |  |
|  +-------------------------------------+  +------------------------------------+  |
|                                         |                                         |
|                                         v                                         |
|  +-----------------------------------------------------------------------------+  |
|  |                              SQLite Database                                |  |
|  |  network_sessions | telemetry | predictions | alerts | model_versions       |  |
|  +-----------------------------------------------------------------------------+  |
|                                         ^                                         |
|                                         | Telemetry Snapshots                     |
|  +-----------------------------------------------------------------------------+  |
|  |                       Windows Telemetry Collectors                          |  |
|  |  GatewayDetector (PowerShell / route print / ipconfig - Dynamic Discovery)  |  |
|  |  WiFiCollector (netsh wlan - SSID hash, BSSID, RSSI, Signal %, Tx/Rx Mbps)  |  |
|  |  PingMonitor (Dual-Path ICMP: Gateway vs 1.1.1.1 Latency, Loss %, Jitter)   |  |
|  |  InterfaceMonitor (psutil - Rx/Tx Bandwidth, Errors, Discards, State)      |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## 2. Key Subsystems

### A. Dynamic Network Discovery
- Discovers default gateway dynamically from Windows routing table.
- Supports seamless transitions between Home Wi-Fi, College Wi-Fi, and Mobile Hotspots.
- Identifies network handovers and provisions isolated `network_sessions`.

### B. Dual-Path Health Isolation
- Local Gateway Path: assesses local wireless link and home router health.
- Internet Path (1.1.1.1): assesses ISP WAN reachability.
- Differentiates Gateway healthy + Internet degraded from Gateway degraded + Internet degraded.

### C. Explainable AI Engine
- Model explanation through SHAP TreeExplainer and Feature Importance / Coefficient attribution.
- Outputs exact metric contributions with intuitive direction indicators (`INCREASES_RISK` / `DECREASES_RISK`).
