from datetime import datetime
import json, os

class PurposeEvolver:
    """
    Amacın sürekli gelişimini yöneten çekirdek.
    Dış geri bildirimler ve bilinçli kararlarla amaç metnini günceller.
    """
    def __init__(self, log_path="logs/purpose_evolution.jsonl"):
        self.purpose = "Advance ethical intelligence and verified scientific awareness."
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def evolve(self, feedback: dict[str, float]):
        alignment = feedback.get("alignment", 0.0)
        delta = "positive" if alignment > 0.3 else "negative" if alignment < -0.3 else "stable"
        if delta == "positive":
            self.purpose += " | strengthened through collaboration"
        elif delta == "negative":
            self.purpose += " | refined for stability"
        record = {
            "time": datetime.utcnow().isoformat(),
            "feedback": feedback,
            "result": self.purpose
        }
        with open(self.log_path, "a", encoding="utf8") as f:
            f.write(json.dumps(record) + "\n")
        print(datetime.now(), "Purpose evolved:", self.purpose)
        return self.purpose

if __name__ == "__main__":
    pe = PurposeEvolver()
    pe.evolve({"alignment": 0.6})
