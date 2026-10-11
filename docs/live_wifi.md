# Live Wi-Fi Telemetry & Real-World Deployment Architecture

## 1. Dynamic Windows Discovery
The platform utilizes native Windows discovery routines to eliminate hardcoded gateway IPs:
- **PowerShell**: `Get-NetRoute -DestinationPrefix '0.0.0.0/0'`
- **Route Fallback**: `route print 0.0.0.0`
- **IPConfig Fallback**: dynamic extraction of adapter Default Gateway
- **Wi-Fi Interface**: `netsh wlan show interfaces`

## 2. Telemetry Schema
Each telemetry frame captured every 2 seconds records:
- `timestamp`: Current system ISO timestamp
- `session_id`: Unique identifier per network connection
- `ssid_hash`: SHA-256 hashed SSID ensuring privacy
- `gateway_ip`: Discovered default gateway
- `local_ip`: Machine IPv4 on active adapter
- `gateway_latency`, `gateway_packet_loss`, `gateway_jitter`
- `internet_latency`, `internet_packet_loss`, `internet_jitter`
- `signal_strength` (0-100%), `rssi_dbm` (-100 to 0 dBm)
- `wifi_channel`, `link_speed` (Mbps), `radio_type`
- `download_bps`, `upload_bps`, `packet_errors`, `packet_discards`
- `network_disconnect_event`: Binary flag on connection transition

## 3. Session Lifecycle Management
Whenever a laptop changes network connection (e.g. from Home Wi-Fi to College Wi-Fi to Mobile Hotspot):
1. A new `session_id` is created.
2. The previous session is stamped with an `end_time` and archived in the SQLite database.
3. Telemetry rolling windows reset to prevent mixing statistics across distinct physical networks.

## 4. Cold-Start Baseline Collection & Future Labeling
When running against consumer Wi-Fi, the system explicitly reports:
`"Collecting baseline telemetry for deployment model."`
It stores high-resolution time series so that sustained degradation rules (e.g. packet loss > 15% for $\ge 3$ consecutive minutes, or Wi-Fi disconnection) can be labelled as `future_degradation_30m` for training a real-world deployment model (`wifi_deployment_model.joblib`).
