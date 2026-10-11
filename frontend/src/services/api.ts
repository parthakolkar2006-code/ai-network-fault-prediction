import {
  NetworkStatus,
  NetworkSession,
  TelemetrySnapshot,
  PredictionResult,
  ModelComparison,
  AblationItem,
  DatasetInfo,
  Alert
} from '../types';

const API_BASE = 'http://localhost:8000/api';

export const api = {
  async getNetworkStatus(): Promise<NetworkStatus> {
    const res = await fetch(`${API_BASE}/network/status`);
    if (!res.ok) throw new Error('Failed to fetch network status');
    return res.json();
  },

  async getNetworkSessions(): Promise<NetworkSession[]> {
    const res = await fetch(`${API_BASE}/network/sessions`);
    if (!res.ok) throw new Error('Failed to fetch sessions');
    return res.json();
  },

  async getCurrentTelemetry(): Promise<TelemetrySnapshot> {
    const res = await fetch(`${API_BASE}/telemetry/current`);
    if (!res.ok) throw new Error('Failed to fetch current telemetry');
    return res.json();
  },

  async getTelemetryHistory(timeframe: string = '1h'): Promise<{ timeframe: string; total_points: number; data: TelemetrySnapshot[] }> {
    const res = await fetch(`${API_BASE}/telemetry/history?timeframe=${timeframe}`);
    if (!res.ok) throw new Error('Failed to fetch telemetry history');
    return res.json();
  },

  async getCurrentPrediction(): Promise<PredictionResult> {
    const res = await fetch(`${API_BASE}/prediction/current`);
    if (!res.ok) throw new Error('Failed to fetch prediction');
    return res.json();
  },

  async getPredictionHistory(): Promise<{ model_version: string; total_points: number; data: any[] }> {
    const res = await fetch(`${API_BASE}/prediction/history`);
    if (!res.ok) throw new Error('Failed to fetch prediction history');
    return res.json();
  },

  async getModelInfo(): Promise<any> {
    const res = await fetch(`${API_BASE}/model/info`);
    if (!res.ok) throw new Error('Failed to fetch model info');
    return res.json();
  },

  async getDatasetInfo(): Promise<DatasetInfo> {
    const res = await fetch(`${API_BASE}/dataset/info`);
    if (!res.ok) throw new Error('Failed to fetch dataset info');
    return res.json();
  },

  async getResearchMetrics(): Promise<ModelComparison[]> {
    const res = await fetch(`${API_BASE}/research/metrics`);
    if (!res.ok) throw new Error('Failed to fetch research metrics');
    return res.json();
  },

  async getResearchCurves(): Promise<{ curves: Record<string, any>; thresholds: Record<string, any> }> {
    const res = await fetch(`${API_BASE}/research/curves`);
    if (!res.ok) throw new Error('Failed to fetch research curves');
    return res.json();
  },

  async getFeatureImportance(): Promise<Array<{ feature: string; importance: number }>> {
    const res = await fetch(`${API_BASE}/research/feature-importance`);
    if (!res.ok) throw new Error('Failed to fetch feature importance');
    return res.json();
  },

  async getAblationResults(): Promise<AblationItem[]> {
    const res = await fetch(`${API_BASE}/research/ablation`);
    if (!res.ok) throw new Error('Failed to fetch ablation results');
    return res.json();
  },

  async getAlerts(): Promise<Alert[]> {
    const res = await fetch(`${API_BASE}/alerts`);
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },

  async simulateBenchmark(
    scenario: 'healthy' | 'moderate' | 'severe',
    custom_overrides?: Record<string, any>
  ): Promise<any> {
    const res = await fetch(`${API_BASE}/prediction/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario, custom_overrides })
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      throw new Error(errData.detail || `Simulation request failed with HTTP ${res.status}`);
    }
    return res.json();
  }
};

