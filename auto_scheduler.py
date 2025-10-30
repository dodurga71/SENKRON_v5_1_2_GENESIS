# =========================================================
#  SENKRON v5.6.0 — auto_scheduler.py
#  Weekly Automation Scheduler for ChronoMatrix Reports
# =========================================================

import time
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import schedule

# -----------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"; LOGS.mkdir(exist_ok=True)
REPORTS = ROOT / "reports"; REPORTS.mkdir(exist_ok=True)
REPORT_SCRIPT = ROOT / "chronomatrix_reporter.py"
LOG_FILE = LOGS / "auto_scheduler.jsonl"

# -----------------------------
def log_event(message: str):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    entry = {"timestamp": ts, "event": message}
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(message)

# -----------------------------
def run_report():
    """Haftalık raporu çalıştırır ve çıktıyı arşivler."""
    log_event("✨ Haftalık rapor oluşturuluyor...")
    try:
        subprocess.run(["py", "-3.11", str(REPORT_SCRIPT)], check=True)
        src = ROOT / "chronomatrix_weekly_report.pdf"
        if src.exists():
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
            dst = REPORTS / f"chronomatrix_weekly_report_{ts}.pdf"
            shutil.copy2(src, dst)
            log_event(f"✅ Rapor üretildi ve arşivlendi: {dst}")
        else:
            log_event("⚠️ Rapor bulunamadı, arşivlenemedi.")
    except subprocess.CalledProcessError as e:
        log_event(f"❌ Rapor çalıştırma hatası: {e}")

# -----------------------------
def main():
    log_event("🧠 SENKRON AutoScheduler başlatıldı.")
    # Her Pazar 03:33'te çalışacak
    schedule.every().sunday.at("03:33").do(run_report)

    log_event("📅 Görev planlandı: Her Pazar 03:33")
    run_report()  # ilk çalıştırma (manuel tetikleme)

    while True:
        schedule.run_pending()
        time.sleep(60)

# -----------------------------
if __name__ == "__main__":
    main()
