export interface TelemetrySnapshot {
  timestamp: string;
  session_id: string;
  ssid_hash?: string;
  gateway_ip?: string;
  local_ip?: string;
  adapter_name?: string;
  connection_state?: string;
  gateway_latency?: number | null;
  gateway_packet_loss?: number | null;
  gateway_jitter?: number | null;
  gateway_reachable?: boolean;
  internet_latency?: number | null;
  internet_packet_loss?: number | null;
  internet_jitter?: number | null;
  internet_reachable?: boolean;
  signal_strength?: number | null;
  rssi_dbm?: number | null;
  wifi_channel?: number | null;
  link_speed?: number | null;
  download_bps?: number;
  upload_bps?: number;
  download_mbps?: number;
  upload_mbps?: number;
  packet_errors?: number;
  packet_discards?: number;
  interface_status?: string;
  network_disconnect_event?: number;
  network_changed?: boolean;
}

export interface ContributingFactor {
  feature: string;
  impact: number;
  value: string | number;
  direction: string;
}

export interface PredictionResult {
  timestamp: string;
  session_id: string;
  is_model_trained: boolean;
  status: string;
  message: string;
  risk_probability?: number | null;
  prediction_state: 'NORMAL' | 'WATCH' | 'ELEVATED' | 'HIGH RISK' | 'BASELINE_COLLECTION' | string;
  threshold?: number | null;
  model_version: string;
  network_health_indicator?: string;
  contributing_factors?: ContributingFactor[];
  engineered_features?: Record<string, any>;
}

export interface NetworkStatus {
  adapter_name?: string;
  connection_state: string;
  ssid_hash?: string;
  gateway_ip?: string;
  local_ip?: string;
  is_gateway_reachable: boolean;
  is_internet_reachable: boolean;
  signal_percent?: number | null;
  channel?: number | null;
  link_speed_mbps?: number | null;
  session_id?: string;
}

export interface NetworkSession {
  session_id: string;
  start_time: string;
  end_time?: string | null;
  ssid_hash: string;
  gateway_ip: string;
  local_ip: string;
  interface_name: string;
  duration_seconds?: number | null;
  avg_gateway_latency?: number | null;
  avg_gateway_loss?: number | null;
  peak_risk?: number | null;
  is_active: boolean;
}

export interface ModelComparison {
  model_name: string;
  optimal_threshold: number;
  test_roc_auc: number;
  test_pr_auc: number;
  test_precision: number;
  test_recall: number;
  test_f1: number;
  test_f2: number;
  test_specificity: number;
  test_fpr: number;
  test_fnr: number;
  confusion_matrix: {
    tp: number;
    fp: number;
    fn: number;
    tn: number;
  };
}

export interface AblationItem {
  feature_group: string;
  feature_count: number;
  optimal_threshold: number;
  pr_auc: number;
  roc_auc: number;
  precision: number;
  recall: number;
  f1: number;
  f2: number;
}

export interface DatasetInfo {
  source: string;
  model_rows: number;
  positive_rows: number;
  negative_rows: number;
  positive_rate: number;
  fault_events: number;
  time_start: string;
  time_end: string;
  feature_count: number;
  features: string[];
  split_info?: any;
  target_definition: string;
  leakage_prevention: string;
}

export interface Alert {
  id?: number;
  timestamp: string;
  severity: 'INFO' | 'WARNING' | 'HIGH' | 'CRITICAL';
  message: string;
  status: string;
}

export interface KeyMetricsSummary {
  icmp_loss_pct: number;
  icmp_loss_max_pct: number;
  icmp_latency_ms: number;
  icmp_jitter_ms: number;
  interface_errors: number;
  interface_discards: number;
  snmp_availability_pct: number;
  total_throughput_mbps: number;
}

export interface SimulationResult {
  scenario: 'healthy' | 'moderate' | 'severe' | string;
  model_name: string;
  risk_probability: number;
  threshold: number;
  prediction_state: string;
  contributing_factors: ContributingFactor[];
  key_metrics_summary: KeyMetricsSummary;
  raw_features_count?: number;
}

