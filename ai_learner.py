# =========================================================
#  SENKRON v5.3.0 — ai_learner.py
#  Self-Adaptive Conscious Learning Engine
#  (Ephemeris + Reflection + Timeline fusion)
# =========================================================

from __future__ import annotations
import os, json
from pathlib import Path
import numpy as np
import pandas as pd
from datetime import datetime

# ---------------------------------------------
#  PATHS
# ---------------------------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)

EPHEMERIS = ROOT / "ephemeris_snapshot.json"
REFLECTION = ROOT / "reflection_trend.json"
TIMELINE = ROOT / "timeline_records.json"
STATE_JSON = ROOT / "ai_state.json"
GENESIS_LOG = LOGS / "genesis_log.jsonl"

# ---------------------------------------------
#  LOG FUNCTION
# ---------------------------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "ai_learner", "message": msg}, ensure_ascii=False) + "\n")
    print(msg, flush=True)

# ---------------------------------------------
#  LOADERS
# ---------------------------------------------
def safe_load_json(path: Path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def normalize_array(arr):
    arr = np.array(arr, dtype=float)
    return (arr - arr.min()) / (np.ptp(arr) + 1e-9)

# ---------------------------------------------
#  CORE FUSION ENGINE
# ---------------------------------------------
def fuse_datasets():
    eph = safe_load_json(EPHEMERIS, {})
    ref = safe_load_json(REFLECTION, [])
    tml = safe_load_json(TIMELINE, {})

    if not eph:
        log("⚠️ Ephemeris verisi yok, failsafe modda öğrenme yapılacak.")
    if not ref:
        log("⚠️ Reflection verisi yok, failsafe momentum 0.5 atanacak.")
    if not tml:
        log("⚠️ Timeline verisi yok, temporal weight 1.0 alınacak.")

    # Ephemeris -> gezegen boylamları
    planets = eph.get("planets") or eph.get("skyfield", {}).get("planets", {})
    planet_values = np.array([v["lon"] for v in planets.values()]) if planets else np.ones(7)
    planet_norm = normalize_array(planet_values)

    # Reflection -> momentum
    reflection_df = pd.DataFrame(ref) if ref else pd.DataFrame([{"momentum": 0.5}])
    reflection_momentum = reflection_df["momentum"].values[-10:] if "momentum" in reflection_df else [0.5]
    momentum_norm = normalize_array(reflection_momentum).mean()

    # Timeline -> accuracy
    timeline_acc = tml.get("mean_accuracy", 1.0)

    # Awareness Gradient
    alpha = float(np.clip(momentum_norm * timeline_acc * planet_norm.mean(), 0.001, 1.0))
    return {
        "timestamp": datetime.now().isoformat(),
        "awareness_gradient": alpha,
        "planet_vector": planet_norm.tolist(),
        "momentum_mean": float(momentum_norm),
        "timeline_acc": float(timeline_acc)
    }

# ---------------------------------------------
#  MAIN EXECUTION
# ---------------------------------------------
def main():
    log("✨ AI Learner Engine başlatılıyor...")
    state = fuse_datasets()

    # Kayıt
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    log(f"🧠 Awareness Gradient (α) = {state['awareness_gradient']:.4f}")
    log("✅ AI Learner tamamlandı.")
    print("🎯 Bilinçsel öğrenme döngüsü başarıyla işlendi.")

if __name__ == "__main__":
    main()
