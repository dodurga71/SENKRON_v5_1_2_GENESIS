# =========================================================
#  SENKRON v5.4.1 — timeline_engine_unified.py
#  Unified Time Continuum Engine
#  Combines MetaPattern + Predictive + Celestial Timelines
# =========================================================

from __future__ import annotations
import json, math, numpy as np, yaml, pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# ---------------------------------------------
#  PATHS
# ---------------------------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
DOCS = ROOT / "docs"

EPHEMERIS = ROOT / "ephemeris_snapshot.json"
AI_STATE  = ROOT / "ai_state.json"
REFLECTION = ROOT / "reflection_trend.json"
SCIENCE = DOCS / "science_registry.yaml"
OUTPUT = ROOT / "timeline_records_unified.json"
GENESIS_LOG = LOGS / "genesis_log.jsonl"

# ---------------------------------------------
#  HELPERS
# ---------------------------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "timeline_engine_unified", "message": msg}, ensure_ascii=False) + "\n")
    print(msg, flush=True)

def safe_load(path: Path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            if path.suffix == ".yaml":
                return yaml.safe_load(f)
            return json.load(f)
    except Exception:
        return default

# ---------------------------------------------
#  META TIMELINE (SCIENCE REGISTRY)
# ---------------------------------------------
def build_metapattern_timeline():
    data = safe_load(SCIENCE, {}) or {}
    records = data.get("records", [])
    if not records:
        return pd.DataFrame(columns=["date","topic","accuracy","novelty"])
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["timestamp"], errors="coerce").dt.strftime("%Y-%m-%d")
    df["accuracy"] = df.get("accuracy_score", 0)
    df["novelty"] = df.get("novelty_score", 0)
    df["topic"] = df.get("title", "Bilinmeyen")
    return df[["date","topic","accuracy","novelty"]]

# ---------------------------------------------
#  PREDICTIVE / CELESTIAL TIMELINE
# ---------------------------------------------
def build_predictive_timeline():
    eph = safe_load(EPHEMERIS, {})
    ai = safe_load(AI_STATE, {})
    ref = safe_load(REFLECTION, [])

    alpha = ai.get("awareness_gradient", 0.25)
    planets = eph.get("planets") or eph.get("skyfield", {}).get("planets", {})
    reflection = ref[-1]["momentum"] if ref else 0.5

    lon_values = [v.get("lon", 0) for v in planets.values()] if planets else [0]*7
    avg_motion = np.mean(np.gradient(lon_values)) if len(lon_values) > 1 else 0.0

    base = datetime.now()
    timeline = []
    for i in range(7):
        date = base + timedelta(days=i)
        tps = np.clip(alpha * (1 + math.sin(avg_motion + i)) * (0.8 + reflection), 0.0, 1.0)
        if tps > 0.75:
            mode, suggestion = "Yüksek Enerji", "Yeni projelere başla, içsel vizyon açık."
        elif tps > 0.45:
            mode, suggestion = "Denge Modu", "Gözlem yap, analiz et, yön belirle."
        else:
            mode, suggestion = "Düşük Enerji", "Dinlen, yeniden şarj ol, içe dön."
        timeline.append({"date": date.strftime("%Y-%m-%d"), "tps": round(float(tps), 3), "energy_mode": mode, "suggestion": suggestion})
    return pd.DataFrame(timeline)

# ---------------------------------------------
#  UNIFICATION LOGIC
# ---------------------------------------------
def unify_timelines():
    df_meta = build_metapattern_timeline()
    df_pred = build_predictive_timeline()

    if df_meta.empty and df_pred.empty:
        log("⚠️ Veri kaynakları boş, zaman çizelgesi oluşturulamadı.")
        return

    if df_meta.empty:
        df_final = df_pred.copy()
    elif df_pred.empty:
        df_final = df_meta.copy()
    else:
        df_final = pd.merge(df_pred, df_meta, on="date", how="outer")
        df_final.fillna({"topic":"-", "accuracy":0, "novelty":0, "tps":0, "energy_mode":"Bilinmiyor", "suggestion":"-"})

    # Özet istatistikler
    mean_acc = round(df_final.get("accuracy", pd.Series([0])).mean(), 3)
    mean_nov = round(df_final.get("novelty", pd.Series([0])).mean(), 3)
    mean_tps = round(df_final.get("tps", pd.Series([0])).mean(), 3)

    summary = {
        "total_records": len(df_final),
        "mean_accuracy": mean_acc,
        "mean_novelty": mean_nov,
        "mean_tps": mean_tps,
        "time_span_days": len(df_final)
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump({
            "unified_timeline": df_final.to_dict(orient="records"),
            "summary": summary
        }, f, ensure_ascii=False, indent=2)

    log(f"🕒 Unified timeline_records_unified.json oluşturuldu. (α={mean_tps}, acc={mean_acc}, nov={mean_nov})")
    return summary

# ---------------------------------------------
#  MAIN
# ---------------------------------------------
def main():
    log("✨ Unified Timeline Engine başlatılıyor...")
    result = unify_timelines()
    if result:
        log("✅ Unified Timeline Engine tamamlandı.")
        print(f"🎯 {result['total_records']} birleşik kayıt üretildi.")
    else:
        print("⚠️ Zaman çizelgesi oluşturulamadı.")

if __name__ == "__main__":
    main()
