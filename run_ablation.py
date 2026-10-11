"""Script to run feature ablation study and save artifacts."""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from ml.ablation import run_ablation_study

if __name__ == "__main__":
    data_path = os.path.join(BACKEND_DIR, "data", "lcore_d_network_future_fault_30m.csv")
    artifacts_dir = os.path.join(BACKEND_DIR, "ml", "artifacts")
    print(f"Starting ablation study on {data_path}...")
    results = run_ablation_study(data_path, artifacts_dir)
    print("\nAblation study completed:")
    import json
    print(json.dumps(results, indent=2))
