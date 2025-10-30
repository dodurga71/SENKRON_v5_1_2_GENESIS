# =========================================================
#  SENKRON v4.1.6+ — self_reflection_visualizer.py
#  Stable Universal Edition (No Deprecation Warnings)
# =========================================================

from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime
import json
import numpy as np
import pandas as pd

# Plotly (tercih) + Kaleido (PNG); hata olursa Matplotlib'e düşer
_PLOTLY_OK = True
try:
    import plotly.graph_objects as go
    import plotly.io as pio  # noqa
except Exception:
    _PLOTLY_OK = False

# Matplotlib fallback
_MPL_OK = True
try:
    import matplotlib.pyplot as plt  # noqa
except Exception:
    _MPL_OK = False

from fpdf import FPDF

# -----------------------------
#  PATHS & CONSTANTS
# -----------------------------
DATA_JSON = "reflection_trend.json"
IMG_PNG = "reflection_curve.png"
HTML_PLOT = "reflection_curve.html"
PDF_FILE = "self_summary.pdf"
FONT_DIR = Path("fonts")
LOG_FILE = Path("logs/reflection_log.txt")

os.makedirs(FONT_DIR, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# -----------------------------
#  FONTS (UTF-8 + Emoji)
# -----------------------------
NOTO_EMOJI_URL = "https://github.com/googlefonts/noto-emoji/raw/main/fonts/NotoColorEmoji.ttf"
DEJAVU_NAME = "DejaVu"
DEJAVU_FILE = FONT_DIR / "DejaVuSans.ttf"   # Manuel kopyalanmalı (Windows)
NOTO_FILE = FONT_DIR / "NotoColorEmoji.ttf" # Otomatik indirilebilir

def ensure_emoji_font():
    """Noto Emoji fontu yoksa indir."""
    if not NOTO_FILE.exists():
        try:
            import urllib.request
            print("🧠 Noto Emoji fontu indiriliyor...")
            urllib.request.urlretrieve(NOTO_EMOJI_URL, NOTO_FILE)
        except Exception as e:
            print(f"⚠️ Noto Emoji indirilemedi: {e}")

ensure_emoji_font()

# -----------------------------
#  LOGGING UTILITY
# -----------------------------
def log_message(message: str):
    """Zaman damgalı log yaz."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

# -----------------------------
#  DATA UTILITIES
# -----------------------------
def generate_reflection_data(days: int = 30) -> pd.DataFrame:
    base = pd.Timestamp.now()
    dates = pd.date_range(base - pd.Timedelta(days=days-1), periods=days, freq="D")
    values = np.cumsum(np.random.randn(days) * 0.2 + 0.5)
    momentum = np.gradient(values)
    df = pd.DataFrame({"date": dates, "reflection_index": values, "momentum": momentum})
    df.to_json(DATA_JSON, orient="records", indent=2, date_format="iso")
    return df

def load_or_repair_data() -> pd.DataFrame:
    """Veriyi yükle veya yeniden oluştur."""
    try:
        if not os.path.exists(DATA_JSON):
            raise FileNotFoundError("json yok")
        df = pd.read_json(DATA_JSON)
        if df.empty or not all(c in df.columns for c in ["date", "reflection_index", "momentum"]):
            raise ValueError("bozuk veri")
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        log_message(f"⚠️ Veri hatası: {e}, yeniden oluşturuluyor...")
        return generate_reflection_data()

# -----------------------------
#  PLOTTING
# -----------------------------
def render_plots(df: pd.DataFrame):
    """Plotly + Kaleido veya Matplotlib ile grafik üret."""
    html_ok = False
    png_ok = False

    if _PLOTLY_OK:
        try:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["date"],
                y=df["reflection_index"],
                mode="lines+markers",
                name="Bilinç İvmesi 🧠",
                line=dict(width=3),
            ))
            fig.update_layout(
                title="SENKRON — Bilinç İvmesi Eğrisi 🧠",
                xaxis_title="Tarih",
                yaxis_title="Reflection Index",
                template="plotly_dark",
                hovermode="x unified",
            )
            fig.write_html(HTML_PLOT)
            html_ok = True

            # Kaleido PNG
            fig.write_image(IMG_PNG)
            png_ok = True
        except Exception as e:
            log_message(f"⚠️ Plotly veya Kaleido hatası: {e}")

    if not png_ok and _MPL_OK:
        try:
            plt.figure(figsize=(10, 5))
            plt.plot(df["date"], df["reflection_index"], marker="o")
            plt.title("SENKRON — Bilinç İvmesi Eğrisi")
            plt.xlabel("Tarih")
            plt.ylabel("Reflection Index")
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig(IMG_PNG, dpi=150)
            plt.close()
            png_ok = True
        except Exception as e:
            log_message(f"⚠️ Matplotlib PNG hatası: {e}")

    # Bilgilendirme
    print(f"{'✅' if html_ok else '⚠️'} Interaktif grafik (HTML): {HTML_PLOT}")
    print(f"{'✅' if png_ok else '⚠️'} Statik grafik (PNG): {IMG_PNG}")

# -----------------------------
#  PDF (FPDF 2.7.6+ uyumlu)
# -----------------------------
class ReflectionPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

        # Fontlar
        if DEJAVU_FILE.exists():
            self.add_font(DEJAVU_NAME, style="", fname=str(DEJAVU_FILE))
            self.add_font(DEJAVU_NAME, style="B", fname=str(DEJAVU_FILE))
            self.set_font(DEJAVU_NAME, size=12)
        else:
            self.set_font("Helvetica", size=12)

        if NOTO_FILE.exists():
            try:
                self.add_font("NotoEmoji", style="", fname=str(NOTO_FILE))
            except Exception:
                pass

        self.add_page()

    def header(self):
        try:
            self.set_font(DEJAVU_NAME, "B", 14)
        except Exception:
            self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "SENKRON — Öz Farkındalık Raporu 🧠",
                  new_x="LMARGIN", new_y="NEXT", align="C")

    def chapter_title(self, title: str):
        try:
            self.set_font(DEJAVU_NAME, "B", 12)
        except Exception:
            self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

    def chapter_body(self, text: str):
        try:
            self.set_font(DEJAVU_NAME, size=11)
        except Exception:
            self.set_font("Helvetica", size=11)
        self.multi_cell(0, 8, text)
        self.ln()

def create_pdf(df: pd.DataFrame):
    """Son bilinç eğilim raporunu PDF olarak oluştur."""
    pdf = ReflectionPDF()
    pdf.chapter_title("1️⃣ Bilinçsel Eğilim Analizi")

    last_value = float(df["reflection_index"].iloc[-1])
    trend = "Yükselişte 🟢" if float(df["momentum"].iloc[-1]) > 0 else "Durağan ⚪"

    summary = (
        f"Son bilinç endeksi: {last_value:.2f}\n"
        f"Eğilim durumu: {trend}\n"
        f"Kayıt tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        "Bu rapor, SENKRON sisteminin öz değerlendirme modülünden otomatik üretilmiştir.\n"
        "Türkçe karakterler ve emojiler mümkün olduğunca uyumludur (PDF fontlarına bağlıdır)."
    )
    pdf.chapter_body(summary)

    if os.path.exists(IMG_PNG):
        try:
            pdf.image(IMG_PNG, x=20, w=170)
        except Exception as e:
            pdf.chapter_body(f"⚠️ Görsel eklenemedi: {e}")

    pdf.output(PDF_FILE)
    print(f"✅ PDF üretildi: {PDF_FILE}")

# -----------------------------
#  MAIN
# -----------------------------
def main():
    df = load_or_repair_data()
    render_plots(df)
    create_pdf(df)
    print("🎯 self_reflection_visualizer başarıyla tamamlandı")
    log_message("✅ self_reflection_visualizer başarıyla tamamlandı.")

if __name__ == "__main__":
    main()
