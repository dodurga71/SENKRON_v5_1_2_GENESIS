# -*- coding: utf-8 -*-
import json, os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, UTC
from matplotlib import font_manager
from fpdf import FPDF

# 🔹 Font seçimi (sessiz mod)
available_fonts = [f.fname for f in font_manager.fontManager.ttflist]
preferred_fonts = ["Arial Unicode MS", "Segoe UI Emoji", "Noto Sans Symbols", "DejaVu Sans"]
selected_font = None
for name in preferred_fonts:
    if any(name.lower() in f.lower() for f in available_fonts):
        selected_font = name
        break
if selected_font:
    plt.rcParams["font.family"] = selected_font
else:
    plt.rcParams["font.family"] = "Arial"

# 🔹 Dosya yolları
metrics_path = "metrics_summary.json"
evolution_log = "self_evolution.log"
output_chart = "evolution_chart.png"
output_pdf = "evolution_report.pdf"

# 🔹 Veriyi yükle
if os.path.exists(evolution_log) and os.path.getsize(evolution_log) > 0:
    df = pd.read_json(evolution_log, lines=True)
else:
    df = pd.DataFrame([{
        "timestamp": datetime.now(UTC).isoformat(),
        "accuracy": 0.0,
        "novelty": 0.0,
        "stability": 1.0
    }])

# 🔹 Eksik kolonları tamamla
for c in ["accuracy", "novelty", "stability"]:
    if c not in df.columns:
        df[c] = 0.0

# 🔹 Görselleştirme
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["accuracy"], marker="o", label="Accuracy")
plt.plot(df["timestamp"], df["novelty"], marker="s", label="Novelty")
plt.plot(df["timestamp"], df["stability"], marker="^", label="Stability")
plt.xlabel("Timestamp (UTC)")
plt.ylabel("Score")
plt.title("SENKRON Evolution Metrics")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(output_chart)
print(f"✅ Görselleştirme tamamlandı → {os.path.abspath(output_chart)}")

# 🔹 Metrik özeti
summary = {
    "mean_accuracy": float(df["accuracy"].mean()),
    "mean_novelty": float(df["novelty"].mean()),
    "mean_stability": float(df["stability"].mean()),
    "entries": len(df),
    "last_update": datetime.now(UTC).isoformat()
}
with open(metrics_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=4, ensure_ascii=False)
print(f"📊 Rapor oluşturuldu → {os.path.abspath(metrics_path)}")

# 🔹 PDF üretimi
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=14)
pdf.cell(200, 10, txt="SENKRON Evolution Report", ln=True, align="C")
pdf.image(output_chart, x=10, y=30, w=190)
pdf.output(output_pdf)
print(f"🧾 PDF raporu oluşturuldu → {os.path.abspath(output_pdf)}")
