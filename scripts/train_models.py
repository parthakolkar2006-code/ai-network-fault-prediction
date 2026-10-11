"""Script to run research model training pipeline and save artifacts."""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

BACKEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from ml.train import run_training_pipeline

if __name__ == "__main__":
    data_path = os.path.join(BACKEND_DIR, "data", "lcore_d_network_future_fault_30m.csv")
    artifacts_dir = os.path.join(BACKEND_DIR, "ml", "artifacts")
    print(f"Starting training on {data_path}...")
    card = run_training_pipeline(data_path, artifacts_dir)
    print("\nTraining completed successfully:")
    import json
    print(json.dumps(card, indent=2))
