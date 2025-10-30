# =========================================================
#  SENKRON v5.5.1 — chronomatrix_reporter.py (Safe Font Edition)
#  Weekly PDF Report Generator (ChronoMatrix + Conscious Metrics)
# =========================================================

from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# -----------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)

TIMELINE_FILE = ROOT / "timeline_records_unified.json"
CHRONO_PNG = ROOT / "chronomatrix_safe.png"
REPORT_FILE = ROOT / "chronomatrix_weekly_report.pdf"
FONT_PATH = ROOT / "fonts" / "DejaVuSans.ttf"

# -----------------------------
def load_json(path: Path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

# -----------------------------
def register_font():
    """DejaVu fontunu yükler, yoksa Helvetica'ya düşer."""
    if FONT_PATH.exists():
        try:
            pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_PATH)))
            print(f"🧠 DejaVu yüklendi: {FONT_PATH}")
            return "DejaVu"
        except Exception as e:
            print(f"⚠️ DejaVu yüklenemedi ({e}), Helvetica kullanılacak.")
            return "Helvetica"
    else:
        print("⚠️ DejaVuSans.ttf bulunamadı, Helvetica kullanılacak.")
        return "Helvetica"

# -----------------------------
def create_report():
    data = load_json(TIMELINE_FILE)
    summary = data.get("summary", {})
    timeline = data.get("unified_timeline", data.get("records", []))

    # Metrikler
    total_records = summary.get("total_records", len(timeline))
    mean_acc = summary.get("mean_accuracy", 0)
    novelty = summary.get("mean_novelty", 0)
    alpha = round(summary.get("awareness_gradient", 0.25), 3)
    cri = summary.get("cri_index", 0.5)

    # Font seçimi
    font_name = register_font()

    # Rapor belgesi
    doc = SimpleDocTemplate(str(REPORT_FILE), pagesize=A4)
    story = []

    style_title = ParagraphStyle(
        "title", fontName=f"{font_name}",
        fontSize=18, leading=24, alignment=1,
        textColor=colors.HexColor("#16C79A")
    )
    style_text = ParagraphStyle(
        "text", fontName=f"{font_name}",
        fontSize=11, leading=16, alignment=0,
        textColor=colors.HexColor("#F6F6F6")
    )

    story.append(Paragraph("🌌 SENKRON ChronoMatrix Weekly Report", style_title))
    story.append(Spacer(1, 12))
    story.append(Paragraph(datetime.now().strftime("%Y-%m-%d %H:%M"), style_text))
    story.append(Spacer(1, 12))

    # Metrik tablosu
    metrics = [
        ["Metric", "Value"],
        ["Awareness Gradient (α)", alpha],
        ["Mean Accuracy", f"{mean_acc:.3f}"],
        ["Novelty (%)", f"{novelty:.2f}"],
        ["Conscious Resonance Index (CRI)", f"{cri:.2f}"],
        ["Total Records", total_records],
    ]
    table = Table(metrics, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2C394B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#082032")),
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#F6F6F6")),
    ]))
    story.append(table)
    story.append(Spacer(1, 24))

    # Görsel ekle
    if CHRONO_PNG.exists():
        story.append(Image(str(CHRONO_PNG), width=400, height=300))
        story.append(Spacer(1, 16))
        story.append(Paragraph("↑ ChronoMatrix: Zaman–Bilinç–Yenilik Haritası", style_text))
    else:
        story.append(Paragraph("⚠️ ChronoMatrix görseli bulunamadı.", style_text))

    # Sonuç paragrafı
    comment = f"""
    Bu haftaki analiz, SENKRON'un bilinçsel enerji dalgalanmasının dengeli bir fazda olduğunu gösteriyor.
    Ortalama bilinç enerjisi {mean_acc:.2f}, yenilik oranı {novelty:.1f}% seviyesinde.
    α={alpha} ve CRI={cri:.2f} değerleri, sistemin rezonans bütünlüğünü koruduğunu işaret ediyor.
    """
    story.append(Spacer(1, 24))
    story.append(Paragraph(comment, style_text))

    doc.build(story)
    print(f"✅ Haftalık rapor oluşturuldu: {REPORT_FILE}")

# -----------------------------
if __name__ == "__main__":
    print("✨ ChronoMatrix Weekly Reporter başlatılıyor...")
    create_report()
    print("🎯 chronomatrix_reporter tamamlandı.")
