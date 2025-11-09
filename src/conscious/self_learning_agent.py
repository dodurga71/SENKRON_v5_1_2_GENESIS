import requests, json
from datetime import datetime
import random, os

class SelfLearningAgent:
    """
    Basit bilimsel öğrenme ajanı.
    İnternetten veri toplar, doğrular ve içsel bilgi tabanına ekler.
    (Gerçek ağ istekleri devre dışıysa sahte veriyle çalışır.)
    """
    def __init__(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.kb_path = os.path.join(base_dir, "data", "knowledge_base.json")
        os.makedirs(os.path.dirname(self.kb_path), exist_ok=True)
        self.knowledge = []
        try:
            with open(self.kb_path, "r", encoding="utf8") as f:
                self.knowledge = json.load(f)
        except FileNotFoundError:
            self.knowledge = []
        print(datetime.now(), "Knowledge entries:", len(self.knowledge))

    def collect(self, topic: str):
        simulated = {"topic": topic, "confidence": round(random.uniform(0.7, 1.0), 2)}
        self.knowledge.append(simulated)
        print(datetime.now(), "Collected:", simulated)
        self.save()

    def validate(self, entry):
        return entry["confidence"] >= 0.8

    def save(self):
        with open(self.kb_path, "w", encoding="utf8") as f:
            json.dump(self.knowledge, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    agent = SelfLearningAgent()
    agent.collect("quantum cognition")
