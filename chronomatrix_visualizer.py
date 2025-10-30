# =========================================================
#  SENKRON v5.4.1 — chronomatrix_visualizer.py
#  Unified Time Continuum Visualizer (3D ChronoMatrix)
# =========================================================

from __future__ import annotations
import os, json
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path

# -----------------------------
ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "timeline_records_unified.json"
OUT_HTML = ROOT / "chronomatrix.html"
OUT_PNG = ROOT / "chronomatrix.png"
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
GENESIS_LOG = LOGS / "genesis_log.jsonl"

# -----------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(msg, flush=True)
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "chronomatrix_visualizer", "message": msg}, ensure_ascii=False) + "\n")

# -----------------------------
def load_data():
    if not DATA_FILE.exists():
        log("❌ timeline_records_unified.json bulunamadı.")
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
def build_chronomatrix(data: dict):
    records = data.get("unified_timeline", [])
    if not records:
        log("⚠️ Veri bulunamadı, çizim atlandı.")
        return

    dates = [r.get("date") for r in records]
    tps = [r.get("tps", 0) for r in records]
    novelty = [r.get("novelty", 0) for r in records]
    accuracy = [r.get("accuracy", 0) for r in records]

    # Normalize novelty for scale
    novelty_scaled = [n / max(novelty) if max(novelty) else 0 for n in novelty]

    fig = go.Figure(data=[go.Scatter3d(
        x=dates,
        y=tps,
        z=novelty_scaled,
        mode="markers+lines",
        marker=dict(
            size=6,
            color=accuracy,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Accuracy"),
            opacity=0.9
        ),
        line=dict(color="white", width=2)
    )])

    fig.update_layout(
        title="SENKRON — 3B ChronoMatrix (Unified Time Continuum)",
        scene=dict(
            xaxis_title="Zaman",
            yaxis_title="Bilinç Enerjisi (TPS)",
            zaxis_title="Yenilik (Novelty)",
            xaxis=dict(showgrid=True, gridcolor="gray", tickangle=-45),
            yaxis=dict(showgrid=True, gridcolor="gray"),
            zaxis=dict(showgrid=True, gridcolor="gray")
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=40),
        height=700
    )

    # Kayıt
    fig.write_html(OUT_HTML)
    try:
        fig.write_image(OUT_PNG)
        log(f"✅ Statik PNG üretildi: {OUT_PNG}")
    except Exception as e:
        log(f"⚠️ PNG üretimi başarısız: {e}")

    log(f"✅ Interaktif HTML üretildi: {OUT_HTML}")
    log("🎯 ChronoMatrix görselleştirme tamamlandı.")

# -----------------------------
def main():
    log("✨ ChronoMatrix Visualizer başlatılıyor...")
    data = load_data()
    if data:
        build_chronomatrix(data)
    else:
        log("❌ Veri yüklenemedi.")
    log("✅ chronomatrix_visualizer tamamlandı.")

if __name__ == "__main__":
    main()
