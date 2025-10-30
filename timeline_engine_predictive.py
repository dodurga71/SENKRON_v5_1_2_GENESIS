# =========================================================
#  SENKRON v5.4.0 — timeline_engine.py
#  Full Solar System + Generational Planets Edition
# =========================================================

from __future__ import annotations
import json, math, numpy as np
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)

EPHEMERIS = ROOT / "ephemeris_snapshot.json"
AI_STATE  = ROOT / "ai_state.json"
REFLECTION = ROOT / "reflection_trend.json"
OUTPUT = ROOT / "timeline_records.json"
GENESIS_LOG = LOGS / "genesis_log.jsonl"

# -----------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "timeline_engine", "message": msg}, ensure_ascii=False) + "\n")
    print(msg, flush=True)

def safe_load(path: Path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

# -----------------------------
def compute_collective_resonance(planets: dict) -> float:
    """Uranüs, Neptün, Plüton arasındaki rezonans (kolektif açı uyumu)."""
    try:
        u, n, p = (planets["Uranus"]["lon"], planets["Neptune"]["lon"], planets["Pluto"]["lon"])
        delta = abs((u - n) % 360 - (n - p) % 360)
        resonance = 1 - abs(math.sin(math.radians(delta)))  # 0-1 arası
        return round(resonance, 4)
    except Exception:
        return 0.5

# -----------------------------
def generate_timeline():
    eph = safe_load(EPHEMERIS, {})
    ai = safe_load(AI_STATE, {})
    ref = safe_load(REFLECTION, [])

    alpha = ai.get("awareness_gradient", 0.25)
    planets = eph.get("planets") or eph.get("skyfield", {}).get("planets", {})
    reflection = ref[-1]["momentum"] if ref else 0.5

    # 🔭 Güneş sistemindeki gezegenler ve jenerasyon objeleri
    planet_list = [
        "Sun", "Mercury", "Venus", "Earth", "Mars",
        "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto",
        "Chiron", "Ceres", "Eris"
    ]

    lon_values = [planets.get(p, {}).get("lon", 180.0) for p in planet_list]
    avg_motion = np.mean(np.gradient(lon_values))
    resonance = compute_collective_resonance(planets)

    # Bilinçsel tahmin formülü
    base = datetime.now()
    timeline = []
    for i in range(7):
        date = base + timedelta(days=i)
        # TPS = Temporal Potential Score
        tps = np.clip(alpha * (1 + math.sin(avg_motion + i)) * (0.8 + reflection + resonance / 2), 0.0, 1.0)
        if tps > 0.75:
            mode, suggestion = "Yüksek Enerji", "Kolektif dönüşüm hızlanıyor, sezgini takip et."
        elif tps > 0.45:
            mode, suggestion = "Denge Modu", "İçsel sessizlikte dış değişimi fark et."
        else:
            mode, suggestion = "Düşük Enerji", "Kendini yeniden kalibre et, dönüşüm yavaş ilerliyor."

        timeline.append({
            "date": date.strftime("%Y-%m-%d"),
            "tps": round(float(tps), 3),
            "energy_mode": mode,
            "suggestion": suggestion
        })

    mean_acc = float(np.mean([d["tps"] for d in timeline]))
    novelty = round(float(np.std([d["tps"] for d in timeline])) * 100, 2)

    data = {
        "total_records": len(timeline),
        "mean_accuracy": round(mean_acc, 3),
        "mean_novelty": novelty,
        "collective_resonance": resonance,
        "records": timeline
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    log(f"🕒 timeline_records.json oluşturuldu. (mean_acc={mean_acc:.3f}, novelty={novelty}, CRI={resonance})")
    return data

# -----------------------------
def main():
    log("✨ Timeline Engine başlatılıyor... (Full Solar System Edition)")
    result = generate_timeline()
    log("✅ Timeline Engine tamamlandı.")
    print(f"🎯 {result['total_records']} günlük tahmin çizelgesi üretildi. (CRI={result['collective_resonance']})")

if __name__ == "__main__":
    main()
