# ==================================================
# timeline_engine.py — SENKRON v4.1.5 MetaPattern & TimeLine Engine
# ==================================================
# Görev:
#   science_registry.yaml içeriğini zaman çizelgesine dönüştürür,
#   öğrenme kalitesine göre istatistiksel özet çıkarır,
#   timeline_records.json dosyasına kaydeder.
# ==================================================

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml

# -------------------------------
# Dosya yolları
# -------------------------------
ROOT = Path(__file__).parent
DATA_PATH = ROOT / "docs" / "science_registry.yaml"
TIMELINE_PATH = ROOT / "timeline_records.json"

# -------------------------------
# Ana fonksiyon
# -------------------------------
def build_timeline():
    """science_registry.yaml içindeki kayıtları okur,
    zaman çizelgesi ve meta pattern korelasyonlarını üretir."""

    if not DATA_PATH.exists():
        print("❌ science_registry.yaml bulunamadı.")
        return

    # YAML içeriğini yükle
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f) or {}

    records = []
    for entry in registry.get("records", []):
        dt = entry.get("timestamp") or datetime.now().isoformat()
        topic = entry.get("title", "Bilinmeyen Başlık")
        acc = entry.get("accuracy_score", 0)
        nov = entry.get("novelty_score", 0)
        records.append({
            "timestamp": dt,
            "topic": topic,
            "accuracy": acc,
            "novelty": nov
        })

    # Kayıt yoksa uyarı
    if len(records) == 0:
        print("⚠️  Kayıt bulunamadı.")
        return

    # DataFrame oluştur
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df.dropna(subset=["timestamp"], inplace=True)
    df.sort_values("timestamp", inplace=True)

    # Özet istatistikleri hesapla
    timeline_summary = {
        "total_records": int(len(df)),
        "mean_accuracy": float(round(df["accuracy"].mean(), 2)),
        "mean_novelty": float(round(df["novelty"].mean(), 2)),
        "time_span_days": int((df["timestamp"].max() - df["timestamp"].min()).days)
    }

    # 🧠 JSON serileştirme hatasını önlemek için timestamp’leri string’e dönüştür
    df["timestamp"] = df["timestamp"].astype(str)

    # timeline_records.json oluştur
    with open(TIMELINE_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "timeline": df.to_dict(orient="records"),
            "summary": timeline_summary
        }, f, indent=2, ensure_ascii=False)

    print(f"🕒 timeline_records.json oluşturuldu. ({timeline_summary})")


# -------------------------------
# Doğrudan çalıştırma
# -------------------------------
if __name__ == "__main__":
    build_timeline()
