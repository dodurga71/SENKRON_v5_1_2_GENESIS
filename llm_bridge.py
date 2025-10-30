# ==================================================
# llm_bridge.py — SENKRON v4.1.5 LLM Evaluation Bridge
# ==================================================

import os, json, time
import openai
from datetime import datetime

# -------------------------------------------
# 1️⃣ API anahtarı kontrolü
# -------------------------------------------
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_KEY"

# -------------------------------------------
# 2️⃣ Metin değerlendirme fonksiyonu
# -------------------------------------------
def evaluate_text(text: str) -> dict:
    """
    Bir bilimsel özeti, doğruluk ve yenilik açısından değerlendirir.
    """
    try:
        prompt = f"""
        Görevin: bilimsel özeti değerlendir.
        Metin: {text}

        Lütfen aşağıdaki formatta JSON üret:
        {{
          "accuracy_score": 0-100 arasında bir sayı,
          "novelty_score": 0-100 arasında bir sayı,
          "summary": "kısa bir açıklama"
        }}
        """

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)
        return data

    except Exception as e:
        return {
            "accuracy_score": 0,
            "novelty_score": 0,
            "summary": f"Hata: {str(e)}"
        }

# -------------------------------------------
# 3️⃣ Test bloğu
# -------------------------------------------
if __name__ == "__main__":
    sample_text = "Bu çalışma metformin ve kurkumin kombinasyonunun nazal beyin iletimine etkisini inceler."
    result = evaluate_text(sample_text)
    print(json.dumps(result, indent=2, ensure_ascii=False))
