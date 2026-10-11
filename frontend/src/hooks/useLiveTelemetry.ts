import { useState, useEffect } from 'react';
import { TelemetrySnapshot, PredictionResult, Alert } from '../types';
import { wsClient } from '../services/websocket';
import { api } from '../services/api';

export function useLiveTelemetry(maxPoints: number = 30) {
  const [telemetry, setTelemetry] = useState<TelemetrySnapshot | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [historyPoints, setHistoryPoints] = useState<TelemetrySnapshot[]>([]);
  const [isConnected, setIsConnected] = useState<boolean>(false);

  useEffect(() => {
    // Initial fetch to load immediately
    api.getCurrentTelemetry().then((t) => {
      if (t && t.session_id) {
        setTelemetry(t);
        setHistoryPoints([t]);
      }
    }).catch(() => {});

    api.getCurrentPrediction().then((p) => {
      if (p) setPrediction(p);
    }).catch(() => {});

    api.getAlerts().then((a) => {
      if (a) setAlerts(a);
    }).catch(() => {});

    // Subscribe to live WebSocket feed
    const unsubscribe = wsClient.subscribe((data) => {
      setIsConnected(true);
      if (data.telemetry) {
        setTelemetry(data.telemetry);
        setHistoryPoints((prev) => {
          const next = [...prev, data.telemetry];
          if (next.length > maxPoints) {
            return next.slice(next.length - maxPoints);
          }
          return next;
        });
      }
      if (data.prediction) {
        setPrediction(data.prediction);
      }
      if (data.alerts && data.alerts.length > 0) {
        setAlerts((prev) => [...data.alerts, ...prev].slice(0, 50));
      }
    });

    return () => {
      unsubscribe();
    };
  }, [maxPoints]);

  return {
    telemetry,
    prediction,
    alerts,
    historyPoints,
    isConnected
  };
}
