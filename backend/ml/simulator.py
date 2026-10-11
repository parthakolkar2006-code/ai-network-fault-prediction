"""
Dedicated Benchmark Simulation Engine for LCORE-D Research Model.
Generates complete 79-feature network telemetry vectors for realistic scenarios:
Healthy Network, Moderate Degradation, and Severe Fault / Pre-Crash.
Computes real ML inference predictions and Explainable AI (XAI) attributions.
"""

import os
import sys
from typing import Dict, Any, Optional

# Ensure backend directory is in sys.path for unpickling
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

import pandas as pd
from ml.inference import InferenceEngine

class NetworkBenchmarkSimulator:
    """
    Simulates network conditions using full 79-feature LCORE-D telemetry profiles.
    Evaluates predictions directly using the trained research benchmark model.
    """
    def __init__(self, artifacts_dir: Optional[str] = None, data_dir: Optional[str] = None):
        if artifacts_dir is None:
            artifacts_dir = os.path.join(os.path.dirname(__file__), "artifacts")
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

        self.artifacts_dir = artifacts_dir
        self.data_dir = data_dir
        self.inference_engine = InferenceEngine(artifacts_dir=self.artifacts_dir)
        self._baseline_profiles: Dict[str, Dict[str, Any]] = {}
        self._init_profiles()

    def _init_profiles(self):
        """Initializes representative scenario baseline feature vectors."""
        csv_path = os.path.join(self.data_dir, "lcore_d_network_future_fault_30m.csv")
        loaded_from_csv = False

        if os.path.exists(csv_path) and self.inference_engine.research_artifact is not None:
            try:
                feature_names = self.inference_engine.research_artifact["feature_names"]
                df = pd.read_csv(csv_path)

                # Representative rows:
                # Row 5113: target=0, 0% loss, stable operational baseline
                # Row 381: moderate degradation (loss ~28.5%, elevated latency)
                # Row 7 / Row 0: severe fault-preceding state (loss 80-100%, high discards)
                if len(df) > 5113:
                    healthy_row = df.loc[5113, feature_names].to_dict()
                    self._baseline_profiles["healthy"] = healthy_row

                if len(df) > 381:
                    moderate_row = df.loc[381, feature_names].to_dict()
                    self._baseline_profiles["moderate"] = moderate_row

                if len(df) > 7:
                    severe_row = df.loc[7, feature_names].to_dict()
                    self._baseline_profiles["severe"] = severe_row

                loaded_from_csv = True
            except Exception as e:
                print(f"Warning: Could not load baseline profiles directly from CSV: {e}")

        # If CSV is not available or fallback needed, construct complete 79-feature baseline
        if not loaded_from_csv or "healthy" not in self._baseline_profiles:
            self._construct_fallback_profiles()

    def _construct_fallback_profiles(self):
        """Constructs complete 79-feature profiles adhering to LCORE-D topology."""
        routers = [f"r{i}" for i in range(1, 8)]

        # 1. Healthy Network Baseline
        healthy: Dict[str, Any] = {
            "icmp_loss_mean": 0.0,
            "icmp_loss_max": 0.0,
            "icmp_loss_std": 0.0,
            "icmp_ping_success_ratio": 1.0,
            "icmp_response_time_mean": 0.053,
            "icmp_response_time_max": 0.120,
            "icmp_response_time_std": 0.015,
            "snmp_availability_mean": 1.0,
            "snmp_unavailable_count": 0,
            "uptime_mean": 32500.0,
            "uptime_min": 32493.0,
            "path_up_ratio": 1.0,
            "path_down_count": 0,
            "downstream_dependents_total": 42,
            "hop_to_server_mean": 3.2,
            "hop_to_core_mean": 1.8,
            "bits_received_total": 4737528.0,
            "bits_sent_total": 4052910.0,
            "interface_error_total": 0,
            "interface_discard_total": 0,
            "interface_down_count": 0,
            "interface_speed_total": 70000.0,
            "interface_count_total": 28
        }
        for r in routers:
            healthy[f"{r}_icmp_loss"] = 0.0
            healthy[f"{r}_icmp_response_time"] = 0.050
            healthy[f"{r}_snmp_availability"] = 1.0
            healthy[f"{r}_uptime"] = 32500.0
            healthy[f"{r}_path_up"] = 1
            healthy[f"{r}_interface_error_total"] = 0
            healthy[f"{r}_interface_discard_total"] = 0
            healthy[f"{r}_interface_down_count"] = 0

        self._baseline_profiles["healthy"] = healthy

        # 2. Moderate Degradation Profile
        moderate = dict(healthy)
        moderate["icmp_loss_mean"] = 24.0
        moderate["icmp_loss_max"] = 45.0
        moderate["icmp_loss_std"] = 18.0
        moderate["icmp_ping_success_ratio"] = 0.76
        moderate["icmp_response_time_mean"] = 0.220
        moderate["icmp_response_time_max"] = 0.550
        moderate["icmp_response_time_std"] = 0.180
        moderate["snmp_availability_mean"] = 0.85
        moderate["interface_error_total"] = 350
        moderate["interface_discard_total"] = 250
        moderate["bits_sent_total"] = 4660846.0
        moderate["bits_received_total"] = 4263775.0
        moderate["r7_icmp_loss"] = 30.0
        moderate["r6_icmp_loss"] = 25.0
        moderate["r2_icmp_loss"] = 20.0
        self._baseline_profiles["moderate"] = moderate

        # 3. Severe Fault Profile
        severe = dict(healthy)
        severe["icmp_loss_mean"] = 92.0
        severe["icmp_loss_max"] = 100.0
        severe["icmp_loss_std"] = 42.0
        severe["icmp_ping_success_ratio"] = 0.08
        severe["icmp_response_time_mean"] = 0.450
        severe["icmp_response_time_max"] = 1.250
        severe["icmp_response_time_std"] = 0.550
        severe["snmp_availability_mean"] = 0.05
        severe["interface_error_total"] = 3500
        severe["interface_discard_total"] = 2400
        severe["bits_sent_total"] = 10132275.0
        severe["bits_received_total"] = 473752.8
        severe["r7_icmp_loss"] = 100.0
        severe["r6_icmp_loss"] = 95.0
        severe["r2_icmp_loss"] = 90.0
        self._baseline_profiles["severe"] = severe

    def generate_scenario_features(
        self,
        scenario: str,
        custom_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Builds a full 79-feature telemetry dictionary for the requested scenario preset.
        Applies domain-consistent perturbations and any user overrides.
        """
        norm_scenario = scenario.strip().lower()

        # If healthy
        if "health" in norm_scenario or norm_scenario == "normal":
            features = dict(self._baseline_profiles["healthy"])
        elif "mod" in norm_scenario or "drop" in norm_scenario:
            features = dict(self._baseline_profiles["moderate"])
        elif "sev" in norm_scenario or "fault" in norm_scenario or "crash" in norm_scenario:
            features = dict(self._baseline_profiles["severe"])
        else:
            raise ValueError(f"Unknown scenario '{scenario}'. Supported presets: 'healthy', 'moderate', 'severe'.")

        if custom_overrides:
            for k, v in custom_overrides.items():
                if v is not None:
                    try:
                        features[k] = float(v)
                    except (ValueError, TypeError):
                        features[k] = v

        return features

    def simulate(
        self,
        scenario: str,
        custom_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end benchmark simulation:
        1. Compiles full 79-feature vector.
        2. Evaluates true ML model prediction and threshold classification.
        3. Computes XAI factor attributions via SHAP / feature coefficients.
        4. Summarizes key simulated telemetry metrics.
        """
        if self.inference_engine.research_artifact is None:
            raise RuntimeError(
                "LCORE-D Research Benchmark model is not loaded. Ensure research_model.joblib is present in artifacts directory."
            )

        features = self.generate_scenario_features(scenario, custom_overrides)
        pred = self.inference_engine.predict_benchmark_sample(features)

        if "error" in pred:
            raise RuntimeError(pred["error"])

        # Extract summary metrics for user-friendly UI display
        key_metrics_summary = {
            "icmp_loss_pct": round(float(features.get("icmp_loss_mean", 0.0)), 2),
            "icmp_loss_max_pct": round(float(features.get("icmp_loss_max", 0.0)), 2),
            "icmp_latency_ms": round(float(features.get("icmp_response_time_mean", 0.0)) * 1000.0, 2),
            "icmp_jitter_ms": round(float(features.get("icmp_response_time_std", 0.0)) * 1000.0, 2),
            "interface_errors": int(features.get("interface_error_total", 0)),
            "interface_discards": int(features.get("interface_discard_total", 0)),
            "snmp_availability_pct": round(float(features.get("snmp_availability_mean", 1.0)) * 100.0, 1),
            "total_throughput_mbps": round(
                (float(features.get("bits_received_total", 0.0)) + float(features.get("bits_sent_total", 0.0))) / 1_000_000.0,
                2
            )
        }

        norm_preset = "healthy"
        if "mod" in scenario.lower():
            norm_preset = "moderate"
        elif "sev" in scenario.lower():
            norm_preset = "severe"

        return {
            "scenario": norm_preset,
            "model_name": pred.get("model_name", "Research Model"),
            "risk_probability": pred.get("risk_probability"),
            "threshold": pred.get("threshold"),
            "prediction_state": pred.get("prediction_state"),
            "contributing_factors": pred.get("contributing_factors", []),
            "key_metrics_summary": key_metrics_summary,
            "raw_features_count": len(features)
        }
