# REST & WebSocket API Specification

## 1. Network Discovery & Status Endpoints
- `GET /api/network/status`: Current adapter name, SSID hash, dynamic Gateway IP, Local IP, reachability status flags, Wi-Fi channel, link speed, and session ID.
- `GET /api/network/interfaces`: List of detected network adapters with operational status (UP/DOWN) and link speed.
- `GET /api/network/session`: Active network session metadata.
- `GET /api/network/sessions`: List of all historically tracked network sessions with duration, avg latency, avg loss, and peak risk.

## 2. Telemetry Endpoints
- `GET /api/telemetry/current`: Latest instantaneous telemetry frame.
- `GET /api/telemetry/history?timeframe={15m|1h|6h|24h|7d}`: Filtered historical time series data.

## 3. Prediction & Explainability Endpoints
- `GET /api/prediction/current`: Current 30-minute degradation probability, operational state (`NORMAL`, `WATCH`, `ELEVATED`, `HIGH RISK`, `BASELINE_COLLECTION`), threshold, and top contributing factors.
- `GET /api/prediction/history`: Time series of prediction risk values.
- `POST /api/prediction/benchmark-test`: Interactive endpoint to evaluate an arbitrary telemetry record against the trained research benchmark model.

## 4. Model & Dataset Transparency Endpoints
- `GET /api/model/info`: Model cards for both the benchmark and deployment models.
- `GET /api/dataset/info`: LCORE-D dataset audit metrics (rows, features, positives, negatives, fault events, temporal split information).

## 5. Research & Evaluation Endpoints
- `GET /api/research/metrics`: Model comparison table with empirical test metrics (ROC-AUC, PR-AUC, Precision, Recall, F1, F2, Confusion Matrix).
- `GET /api/research/curves`: ROC curves, Precision-Recall curves, and Threshold optimization curves.
- `GET /api/research/feature-importance`: Ranked list of top 25 features by importance.
- `GET /api/research/ablation`: Results of empirical feature ablation experiments.
- `POST /api/research/retrain`: Triggers model re-training in the background.

## 6. Alerts Endpoint
- `GET /api/alerts`: Recent network alerts with severity and cooldown debounce status.

## 7. Real-Time WebSocket Channel
- `WS /ws/live`: Streams live telemetry snapshots and predictions every 2 seconds.
