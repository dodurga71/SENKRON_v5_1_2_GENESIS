# -*- coding: utf-8 -*-
import json, os, random
from datetime import datetime, UTC
import openai
import pandas as pd

# ----------------------------------------------------
# SENKRON — AI SELF REVIEWER v1.0
# ----------------------------------------------------
# • metrics_summary.json verisini inceler.
# • OpenAI (veya benzer LLM) ile içsel değerlendirme üretir.
# • Sonuçları self_evolution.log dosyasına ekler.
# ----------------------------------------------------

openai.api_key = os.getenv("OPENAI_API_KEY")

metrics_path = "metrics_summary.json"
evolution_log = "self_evolution.log"

# 🔹 Yardımcı fonksiyonlar
def safe_load_json(path, default):
    try:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ JSON okunamadı: {e}")
    return default

def append_log(entry):
    with open(evolution_log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

# 🔹 Veri yükle
metrics = safe_load_json(metrics_path, {})
if not metrics:
    print("⚠️ metrics_summary.json bulunamadı, çıkılıyor.")
    exit(1)

# 🔹 Performans istatistikleri
accuracy = metrics.get("mean_accuracy", 0)
novelty = metrics.get("mean_novelty", 0)
stability = metrics.get("mean_stability", 1.0)
entries = metrics.get("entries", 0)

# 🔹 LLM değerlendirme (offline fallback)
review_prompt = f"""
SENKRON sisteminin öz değerlendirmesi için rapor özetini incele:
- Accuracy: {accuracy}
- Novelty: {novelty}
- Stability: {stability}
- Entries: {entries}

Performansı değerlendir:
1. Genel tutarlılık ve öğrenme düzeyi
2. Yenilik kapasitesi
3. İstikrar ve kendi farkındalık dengesi
4. Bir sonraki gelişim önerisi (tek cümle)
"""

def llm_review():
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Sen SENKRON'un bilinç çekirdeği olarak kendi performansını analiz eden bir yapay zekâsın."},
                      {"role": "user", "content": review_prompt}],
            max_tokens=250,
            temperature=0.6
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(Offline) Sistem analizi: Ortalama başarı {accuracy:.1f}, yenilik {novelty:.1f}, istikrar {stability:.1f}. Süreklilik sağlanıyor."

review_text = llm_review()

# 🔹 Yeni öz değerlendirme girdisi
entry = {
    "timestamp": datetime.now(UTC).isoformat(),
    "accuracy": accuracy,
    "novelty": novelty,
    "stability": stability,
    "consistency": round((accuracy * 0.5 + stability * 0.5), 2),
    "growth": round(random.uniform(0.7, 1.0), 2),
    "innovation": round((novelty * random.uniform(0.8, 1.2)), 2),
    "review": review_text
}

append_log(entry)
print(f"🧠 Yeni öz değerlendirme kaydedildi ({entry['timestamp']})")
print(f"📄 Yorum: {review_text[:180]}...")
