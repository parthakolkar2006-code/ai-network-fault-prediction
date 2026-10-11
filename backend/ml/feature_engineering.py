"""
Feature Engineering for LCORE-D benchmark modeling and Real Wi-Fi live telemetry.
Strictly causal: uses only current and past observations, never future data.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# 79 research features from LCORE-D
RESEARCH_FEATURES = [
    "icmp_loss_mean", "icmp_loss_max", "icmp_loss_std", "icmp_ping_success_ratio",
    "icmp_response_time_mean", "icmp_response_time_max", "icmp_response_time_std",
    "snmp_availability_mean", "snmp_unavailable_count", "uptime_mean", "uptime_min",
    "path_up_ratio", "path_down_count", "downstream_dependents_total",
    "hop_to_server_mean", "hop_to_core_mean", "bits_received_total", "bits_sent_total",
    "interface_error_total", "interface_discard_total", "interface_down_count",
    "interface_speed_total", "interface_count_total",
    "r1_icmp_loss", "r1_icmp_response_time", "r1_snmp_availability", "r1_uptime", "r1_path_up", "r1_interface_error_total", "r1_interface_discard_total", "r1_interface_down_count",
    "r2_icmp_loss", "r2_icmp_response_time", "r2_snmp_availability", "r2_uptime", "r2_path_up", "r2_interface_error_total", "r2_interface_discard_total", "r2_interface_down_count",
    "r3_icmp_loss", "r3_icmp_response_time", "r3_snmp_availability", "r3_uptime", "r3_path_up", "r3_interface_error_total", "r3_interface_discard_total", "r3_interface_down_count",
    "r4_icmp_loss", "r4_icmp_response_time", "r4_snmp_availability", "r4_uptime", "r4_path_up", "r4_interface_error_total", "r4_interface_discard_total", "r4_interface_down_count",
    "r5_icmp_loss", "r5_icmp_response_time", "r5_snmp_availability", "r5_uptime", "r5_path_up", "r5_interface_error_total", "r5_interface_discard_total", "r5_interface_down_count",
    "r6_icmp_loss", "r6_icmp_response_time", "r6_snmp_availability", "r6_uptime", "r6_path_up", "r6_interface_error_total", "r6_interface_discard_total", "r6_interface_down_count",
    "r7_icmp_loss", "r7_icmp_response_time", "r7_snmp_availability", "r7_uptime", "r7_path_up", "r7_interface_error_total", "r7_interface_discard_total", "r7_interface_down_count"
]

FEATURE_GROUPS = {
    "icmp_only": [
        c for c in RESEARCH_FEATURES if "icmp" in c or "ping" in c or "response_time" in c
    ],
    "icmp_snmp": [
        c for c in RESEARCH_FEATURES if "icmp" in c or "ping" in c or "response_time" in c or "snmp" in c or "uptime" in c
    ],
    "icmp_snmp_interface": [
        c for c in RESEARCH_FEATURES if not ("hop" in c or "dependent" in c or "path" in c)
    ],
    "all_telemetry": RESEARCH_FEATURES
}

class ResearchDataPreprocessor:
    """Preprocesses research benchmark tabular data with median imputation and scaling."""
    def __init__(self, feature_cols: Optional[List[str]] = None):
        self.feature_cols = feature_cols or RESEARCH_FEATURES
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        self.is_fitted = False

    def fit(self, X: pd.DataFrame):
        X_sub = X[self.feature_cols]
        X_imp = self.imputer.fit_transform(X_sub)
        self.scaler.fit(X_imp)
        self.is_fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before transform")
        X_sub = X[self.feature_cols]
        # Compatibility fix: ensure _fill_dtype exists on SimpleImputer across scikit-learn versions
        if hasattr(self.imputer, "statistics_") and not hasattr(self.imputer, "_fill_dtype"):
            try:
                self.imputer._fill_dtype = self.imputer.statistics_.dtype
            except Exception:
                pass
        X_imp = self.imputer.transform(X_sub)
        return self.scaler.transform(X_imp)

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.fit(X).transform(X)


class LiveWiFiFeatureExtractor:
    """
    Computes rolling metrics and stability indicators over real-time laptop Wi-Fi telemetry.
    Strictly past-only windows: 1m, 5m, 10m, 15m, 30m.
    """
    def __init__(self):
        pass

    def compute_features(self, history_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Takes historical telemetry DataFrame for current session (sorted by timestamp ascending).
        Returns engineered features for the latest observation.
        """
        if history_df.empty:
            return {}

        df = history_df.copy()
        if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp").reset_index(drop=True)

        latest = df.iloc[-1]
        now = latest["timestamp"]

        # Time windows
        w1m = df[df["timestamp"] >= now - pd.Timedelta(minutes=1)]
        w5m = df[df["timestamp"] >= now - pd.Timedelta(minutes=5)]
        w10m = df[df["timestamp"] >= now - pd.Timedelta(minutes=10)]
        w15m = df[df["timestamp"] >= now - pd.Timedelta(minutes=15)]
        w30m = df[df["timestamp"] >= now - pd.Timedelta(minutes=30)]

        gw_lat = latest.get("gateway_latency", 0.0) or 0.0
        inet_lat = latest.get("internet_latency", 0.0) or 0.0
        gw_loss = latest.get("gateway_packet_loss", 0.0) or 0.0
        inet_loss = latest.get("internet_packet_loss", 0.0) or 0.0

        # Gateway vs Internet differences
        gw_inet_lat_diff = float(inet_lat - gw_lat)
        gw_inet_loss_diff = float(inet_loss - gw_loss)

        # 5m aggregations
        gw_lat_mean_5m = float(w5m["gateway_latency"].mean()) if "gateway_latency" in w5m and len(w5m) > 0 else gw_lat
        gw_lat_std_5m = float(w5m["gateway_latency"].std()) if "gateway_latency" in w5m and len(w5m) > 1 else 0.0
        gw_lat_max_5m = float(w5m["gateway_latency"].max()) if "gateway_latency" in w5m and len(w5m) > 0 else gw_lat

        gw_loss_mean_5m = float(w5m["gateway_packet_loss"].mean()) if "gateway_packet_loss" in w5m and len(w5m) > 0 else gw_loss
        gw_loss_max_5m = float(w5m["gateway_packet_loss"].max()) if "gateway_packet_loss" in w5m and len(w5m) > 0 else gw_loss

        inet_lat_mean_5m = float(w5m["internet_latency"].mean()) if "internet_latency" in w5m and len(w5m) > 0 else inet_lat
        inet_loss_mean_5m = float(w5m["internet_packet_loss"].mean()) if "internet_packet_loss" in w5m and len(w5m) > 0 else inet_loss

        signal_mean_5m = float(w5m["signal_strength"].mean()) if "signal_strength" in w5m and len(w5m) > 0 and w5m["signal_strength"].notnull().any() else (latest.get("signal_strength") or 0.0)
        signal_min_5m = float(w5m["signal_strength"].min()) if "signal_strength" in w5m and len(w5m) > 0 and w5m["signal_strength"].notnull().any() else (latest.get("signal_strength") or 0.0)

        # Changes (latest vs 5m ago average)
        lat_change = float(gw_lat - gw_lat_mean_5m)
        loss_change = float(gw_loss - gw_loss_mean_5m)
        signal_change = float((latest.get("signal_strength") or 0.0) - signal_mean_5m)

        # Consecutive packet loss
        consecutive_losses = 0
        for val in reversed(df["gateway_packet_loss"].tolist()):
            if val and val > 0:
                consecutive_losses += 1
            else:
                break

        # Disconnect count in 15m
        disconnect_count_15m = 0
        if "network_disconnect_event" in w15m:
            disconnect_count_15m = int(w15m["network_disconnect_event"].fillna(0).sum())

        # Instability score: 0 to 100
        # Components: loss (40%), jitter/latency variance (30%), signal drop (20%), disconnects (10%)
        instability = min(100.0, (
            (gw_loss_mean_5m * 0.4) +
            (min(gw_lat_std_5m, 100.0) * 0.3) +
            (max(0.0, (70.0 - float(latest.get("signal_strength") or 70.0))) * 0.4) +
            (disconnect_count_15m * 20.0)
        ))

        return {
            "timestamp": str(now),
            "gateway_latency_mean_5m": round(gw_lat_mean_5m, 2),
            "gateway_latency_std_5m": round(gw_lat_std_5m, 2),
            "gateway_latency_max_5m": round(gw_lat_max_5m, 2),
            "gateway_packet_loss_mean_5m": round(gw_loss_mean_5m, 2),
            "gateway_packet_loss_max_5m": round(gw_loss_max_5m, 2),
            "internet_latency_mean_5m": round(inet_lat_mean_5m, 2),
            "internet_packet_loss_mean_5m": round(inet_loss_mean_5m, 2),
            "signal_mean_5m": round(signal_mean_5m, 1),
            "signal_min_5m": round(signal_min_5m, 1),
            "latency_change": round(lat_change, 2),
            "packet_loss_change": round(loss_change, 2),
            "signal_change": round(signal_change, 1),
            "gateway_vs_internet_latency_diff": round(gw_inet_lat_diff, 2),
            "gateway_vs_internet_loss_diff": round(gw_inet_loss_diff, 2),
            "consecutive_packet_loss_count": consecutive_losses,
            "disconnect_count_15m": disconnect_count_15m,
            "network_instability_score": round(instability, 2)
        }
