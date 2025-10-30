# ==================================================
# self_evolution.py — SENKRON v4.1.5 Conscious Growth Logger (Final UTC Version)
# ==================================================
# Görev:
#   Sistem içindeki her öğrenme ve güncelleme olayını
#   endüstriyel formatta (JSONL) kaydeder.
#   Olay tipi, zaman, skor değişimleri ve stabilite
#   indeksini hesaplayarak self_evolution.log’a yazar.
# ==================================================

import json
import os
import statistics
from datetime import datetime, UTC
from pathlib import Path

LOG_PATH = Path(__file__).parent / "self_evolution.log"
TIMELINE_PATH = Path(__file__).parent / "timeline_records.json"


def calculate_stability(accuracy_list, novelty_list):
    """Accuracy ve novelty skorlarından stability index hesaplar."""
    if len(accuracy_list) < 2 or len(novelty_list) < 2:
        return 1.0
    acc_var = statistics.pstdev(accuracy_list)
    nov_var = statistics.pstdev(novelty_list)
    return round(max(0.0, 1.0 - (acc_var + nov_var) / 200), 3)  # 0–1 arası denge ölçütü


def log_evolution(phase: str):
    """Zaman çizelgesinden verileri okuyarak self_evolution.log’a kayıt atar."""
    if not TIMELINE_PATH.exists():
        print("⚠️ timeline_records.json bulunamadı — kayıt yapılmadı.")
        return

    with open(TIMELINE_PATH, "r", encoding="utf-8") as f:
        timeline = json.load(f)

    records = timeline.get("timeline", [])
    acc_list = [r.get("accuracy", 0) for r in records]
    nov_list = [r.get("novelty", 0) for r in records]
    summary = timeline.get("summary", {})

    stability_index = calculate_stability(acc_list, nov_list)
    last_acc = float(summary.get("mean_accuracy", 0))
    last_nov = float(summary.get("mean_novelty", 0))
    total_records = int(summary.get("total_records", 0))

    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(timespec="milliseconds"),
        "phase": phase,
        "records": total_records,
        "mean_accuracy": last_acc,
        "mean_novelty": last_nov,
        "stability_index": stability_index,
        "delta_learn": round((last_acc + last_nov) / 200, 3)
    }

    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    print(f"🧬 self_evolution.log güncellendi → {phase} | stability={stability_index}")


if __name__ == "__main__":
    log_evolution("timeline_update")