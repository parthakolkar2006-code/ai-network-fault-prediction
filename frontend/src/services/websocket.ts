import { TelemetrySnapshot, PredictionResult, Alert } from '../types';

export type LiveMessageCallback = (data: {
  telemetry: TelemetrySnapshot;
  prediction: PredictionResult;
  alerts: Alert[];
}) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private url: string = 'ws://localhost:8000/ws/live';
  private listeners: Set<LiveMessageCallback> = new Set();
  private isConnecting: boolean = false;
  private reconnectInterval: number = 2000;

  connect() {
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }
    this.isConnecting = true;

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        this.isConnecting = false;
        console.log('[WebSocket] Connected to live telemetry stream');
      };

      this.ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'TICK' || payload.type === 'SNAPSHOT') {
            this.listeners.forEach((callback) => {
              callback({
                telemetry: payload.telemetry,
                prediction: payload.prediction,
                alerts: payload.alerts || []
              });
            });
          }
        } catch (e) {
          console.error('[WebSocket] Failed to parse message', e);
        }
      };

      this.ws.onclose = () => {
        this.isConnecting = false;
        this.ws = null;
        setTimeout(() => this.connect(), this.reconnectInterval);
      };

      this.ws.onerror = (err) => {
        console.warn('[WebSocket] Error:', err);
        if (this.ws) {
          this.ws.close();
        }
      };
    } catch (e) {
      this.isConnecting = false;
      setTimeout(() => this.connect(), this.reconnectInterval);
    }
  }

  subscribe(callback: LiveMessageCallback) {
    this.listeners.add(callback);
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.connect();
    }
    return () => {
      this.listeners.delete(callback);
    };
  }
}

export const wsClient = new WebSocketClient();
