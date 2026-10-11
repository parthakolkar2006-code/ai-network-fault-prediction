# Explainable AI Framework for Predictive Network Fault Detection & Wi-Fi Degradation System

**Research Title:**  
*"An Explainable AI Framework for Predictive Network Fault Detection Using SNMP and Network Performance Metrics"*

**Practical Application Extension:**  
*"AI-Based Intelligent Wi-Fi Network Degradation and Fault Prediction"*

---

## 1. Project Overview & Objective

This repository contains an end-to-end, research-grade, and deployable AI network operations platform. It combines:
1. **Research Benchmark Engine**: Evaluates 5 machine learning architectures on the authoritative **LCORE-D v2** dataset (22,381 rows, 79 features, ~5% rare-event class balance, 69 logged fault events) using chronological embargo splitting and validation threshold optimization.
2. **Real Laptop Wi-Fi Telemetry Engine**: Dynamically detects the laptop's active network adapter, connected SSID, and default gateway without hardcoding IP addresses. Collects dual-path latency, packet loss, and jitter (Local Gateway vs Internet 1.1.1.1) alongside link speed, signal strength, and bandwidth.
3. **Domain-Shift Integrity**: Adheres strictly to scientific integrity by clearly separating the ISP research benchmark from live laptop Wi-Fi monitoring. It displays an honest cold-start baseline telemetry state instead of fabricating predictions.
4. **NOC Modern Dashboard**: A web dashboard built in React 18, TypeScript, Tailwind CSS, Lucide Icons, and Recharts, with live WebSocket data streaming.

---

## 2. System Architecture

```
network_fault_ai/
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app and 2s background telemetry loop
│   │   ├── api/                 # REST routers (network, telemetry, prediction, model, dataset, research, alerts)
│   │   ├── websocket/           # WebSocket connection manager (/ws/live)
│   │   ├── services/            # Session, telemetry, prediction, and alert services
│   │   ├── models/              # SQLAlchemy models (sessions, telemetry, predictions, alerts, versions)
│   │   ├── schemas/             # Pydantic validation schemas
│   │   └── database/            # Database session and SQLite engine
│   │
│   ├── collectors/
│   │   ├── gateway_detector.py  # Dynamic Windows gateway discovery (Get-NetRoute, route print, ipconfig)
│   │   ├── wifi_collector.py    # Windows netsh wlan parser with SSID SHA-256 hashing
│   │   ├── ping_monitor.py      # Dual-path concurrent ICMP ping (Gateway vs 1.1.1.1)
│   │   ├── interface_monitor.py # psutil bandwidth, errors, discards, and link state
│   │   └── network_discovery.py # Session lifecycle and network change orchestrator
│   │
│   ├── ml/
│   │   ├── split.py             # Chronological split with 30m embargo buffer
│   │   ├── feature_engineering.py # Preprocessing & 1m/5m/10m/15m/30m rolling features
│   │   ├── train.py             # Trains LR, RF, HistGB, XGBoost, LightGBM + threshold tuning
│   │   ├── evaluate.py          # Real metrics, ROC/PR curves, confusion matrices
│   │   ├── ablation.py          # Systematic feature ablation across 5 telemetry subsets
│   │   ├── explainability.py    # SHAP and local feature attribution
│   │   ├── inference.py         # Domain-shift-safe inference engine
│   │   └── artifacts/           # Trained models, cards, metrics, and curve JSONs
│   │
│   ├── data/                    # LCORE-D CSVs and dataset audit metadata
│   ├── tests/                   # 20 unit and integration tests (100% passing)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Sidebar, Header, MetricCard, StatusBadge
│   │   ├── pages/               # Overview, LiveMonitoring, AIPrediction, History, Sessions, Dataset, Research
│   │   ├── hooks/               # useLiveTelemetry WebSocket & polling hook
│   │   ├── services/            # REST and WebSocket clients
│   │   └── types/               # TypeScript interfaces
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── scripts/
│   ├── train_models.py          # Script to run multi-model training pipeline
│   └── run_ablation.py          # Script to run feature ablation experiments
│
├── docs/                        # In-depth architectural & research documentation
├── start_backend.bat            # One-click backend startup script
├── start_frontend.bat           # One-click frontend startup script
└── start_all.bat                # Master launcher for both backend & frontend
```

---

## 3. Empirical Research Benchmark Results

All metrics are computed from actual ML training on `lcore_d_network_future_fault_30m.csv` using a 70% Train, 15% Validation, 15% Test chronological split with a 30-minute embargo buffer:

| Model Architecture | Optimal Threshold | PR-AUC | ROC-AUC | Precision | Recall | F1 Score | F2 Score | Test FPR |
|---|---|---|---|---|---|---|---|---|
| **HistGradientBoosting** | 0.01 | **0.1828** | 0.4003 | 11.8% | **68.5%** | **0.2011** | **0.3491** | 85.5% |
| **Random Forest** | 0.01 | **0.2207** | **0.5693** | **19.8%** | 64.2% | **0.3032** | **0.4437** | 43.2% |
| **LightGBM** | 0.01 | 0.1671 | 0.4312 | 12.1% | 35.8% | 0.1804 | 0.2569 | 43.5% |
| **XGBoost** | 0.01 | 0.1512 | 0.4193 | 16.0% | 9.3% | 0.1172 | 0.1011 | **8.1%** |
| **Logistic Regression** | 0.38 | 0.1508 | 0.3822 | 8.5% | 17.3% | 0.1143 | 0.1434 | 30.9% |

### Feature Ablation Study

Evaluated across isolated feature subsets to determine telemetric predictive contribution:

| Feature Subset | Feature Count | PR-AUC | ROC-AUC | Precision | Recall | F1 Score |
|---|---|---|---|---|---|---|
| **ICMP-only features** | 21 | 0.1580 | 0.5298 | 15.9% | 35.8% | 0.2197 |
| **ICMP + SNMP** | 39 | 0.1415 | 0.4778 | 9.7% | 8.0% | 0.0878 |
| **ICMP + SNMP + Interface metrics** | 67 | **0.1821** | 0.4853 | 14.5% | **49.4%** | **0.2244** |
| **All network telemetry features** | 23 | **0.1854** | 0.4705 | 13.4% | 29.0% | 0.1832 |
| **All telemetry + router topology** | 79 | 0.1671 | 0.4312 | 12.1% | 35.8% | 0.1804 |

---

## 4. Running the Project (Windows Setup)

### Quick One-Click Startup
Double click:
```cmd
start_all.bat
```
This automatically launches:
- **Backend API & WebSocket server** at `http://localhost:8000`
- **Frontend NOC Dashboard** at `http://localhost:5173`

---

### Manual Startup

#### 1. Backend Server
```powershell
cd network_fault_ai\backend
python -m pip install -r requirements.txt
$env:PYTHONPATH='.'
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Development Server
```powershell
cd network_fault_ai\frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 5. Automated Tests

The backend test suite contains 20 automated unit and integration tests covering gateway detection, Wi-Fi collection, ping monitoring, temporal splits, feature engineering, cold-start inference, and FastAPI routes:

```powershell
cd network_fault_ai
$env:PYTHONPATH='backend'
python -m pytest backend\tests -v -p no:cacheprovider
```

Result:
```
============================= 20 passed in 15.77s =============================
```

---

## 6. Research & Scientific Integrity
- **No Fabricated Metrics**: Every metric, curve, and threshold displayed on the dashboard is loaded directly from real experiment runs.
- **Domain Shift Awareness**: LCORE-D core ISP benchmark models are isolated from consumer edge Wi-Fi connections.
- **Privacy Compliance**: All SSIDs are SHA-256 hashed and raw IP addresses are excluded from ML features.
