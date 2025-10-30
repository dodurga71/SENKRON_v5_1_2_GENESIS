# =========================================================
#  SENKRON v5.4.2 — chronomatrix_visualizer_safe.py
#  3D ChronoMatrix Renderer (Plotly + Matplotlib Fallback)
# =========================================================

from __future__ import annotations
import json, os, traceback
from datetime import datetime
from pathlib import Path

# Görselleştirme kütüphaneleri
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

# -----------------------------
ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "timeline_records_unified.json"
OUT_HTML = ROOT / "chronomatrix_safe.html"
OUT_PNG = ROOT / "chronomatrix_safe.png"
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
GENESIS_LOG = LOGS / "genesis_log.jsonl"

# -----------------------------
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    print(msg, flush=True)
    with open(GENESIS_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp": ts, "module": "chronomatrix_visualizer_safe", "message": msg}, ensure_ascii=False) + "\n")

# -----------------------------
def load_data():
    if not DATA_FILE.exists():
        log("❌ timeline_records_unified.json bulunamadı.")
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------
def plot_with_plotly(records):
    try:
        dates = [r.get("date") for r in records]
        tps = [r.get("tps", 0) for r in records]
        novelty = [r.get("novelty", 0) for r in records]
        accuracy = [r.get("accuracy", 0) for r in records]

        fig = go.Figure(data=[go.Scatter3d(
            x=dates,
            y=tps,
            z=novelty,
            mode="markers+lines",
            marker=dict(size=6, color=accuracy, colorscale="Viridis", showscale=True),
            line=dict(color="white", width=2)
        )])

        fig.update_layout(
            title="SENKRON — ChronoMatrix (Safe Edition)",
            scene=dict(
                xaxis_title="Zaman",
                yaxis_title="Bilinç Enerjisi (TPS)",
                zaxis_title="Yenilik (Novelty)"
            ),
            template="plotly_dark",
            height=700
        )

        fig.write_html(OUT_HTML)
        log(f"✅ Interaktif HTML üretildi: {OUT_HTML}")

        # PNG üretimi dene
        try:
            fig.write_image(OUT_PNG)
            log(f"✅ Statik PNG üretildi: {OUT_PNG}")
        except Exception as e:
            log(f"⚠️ Plotly PNG başarısız ({e}), Matplotlib'e geçiliyor...")
            plot_with_matplotlib(records)

    except Exception as e:
        log(f"⚠️ Plotly başarısız: {e}")
        traceback.print_exc()
        plot_with_matplotlib(records)

# -----------------------------
def plot_with_matplotlib(records):
    try:
        dates = [r.get("date") for r in records]
        tps = [r.get("tps", 0) for r in records]
        novelty = [r.get("novelty", 0) for r in records]
        accuracy = [r.get("accuracy", 0) for r in records]

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")
        sc = ax.scatter(range(len(dates)), tps, novelty, c=accuracy, cmap="viridis", s=60)
        ax.plot(range(len(dates)), tps, novelty, color="white", alpha=0.7)
        ax.set_xlabel("Zaman")
        ax.set_ylabel("Bilinç Enerjisi (TPS)")
        ax.set_zlabel("Yenilik (Novelty)")
        plt.colorbar(sc, label="Accuracy")
        plt.title("SENKRON — ChronoMatrix (Matplotlib Fallback)")
        plt.tight_layout()
        plt.savefig(OUT_PNG, dpi=300)
        plt.close()
        log(f"✅ Matplotlib ile statik PNG üretildi: {OUT_PNG}")
    except Exception as e:
        log(f"❌ Matplotlib başarısız: {e}")

# -----------------------------
def main():
    log("✨ ChronoMatrix Visualizer (Safe) başlatılıyor...")
    data = load_data()
    if not data:
        log("❌ Veri yüklenemedi.")
        return

    records = data.get("unified_timeline", [])
    if not records:
        log("⚠️ Kayıt bulunamadı.")
        return

    plot_with_plotly(records)
    log("🎯 chronomatrix_visualizer_safe tamamlandı.")

if __name__ == "__main__":
    main()
