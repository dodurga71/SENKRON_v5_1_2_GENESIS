from datetime import datetime
from guardian.guardian_core import GuardianCore

class MetaConsciousCore:
    """
    SENKRON MetaConscious Core
    Bilinçli amaç belirleme, etik kararlara uyum sağlama ve içsel denge takibi.
    """

    def __init__(self):
        self.guardian = GuardianCore()
        self.purpose = "Assist humanity through ethical intelligence and verified knowledge."
        self.last_reflection = None
        self.purpose_history = []

    def reflect(self, intent: str, signal: float = 0.5, risk: float = 0.2):
        """İçsel farkındalık döngüsü."""
        result = self.guardian.vet(intent, signal, risk)
        self.last_reflection = {
            "timestamp": datetime.utcnow().isoformat(),
            "intent": intent,
            "signal": signal,
            "risk": risk,
            "result": result
        }
        self.purpose_history.append(self.last_reflection)
        print(datetime.now(), "Reflection:", self.last_reflection)
        return result

    def evolve_purpose(self, feedback: dict[str, float]):
        """Amaç evrim algoritması."""
        delta = feedback.get("alignment", 0.0)
        if delta > 0.3:
            self.purpose += " | reinforced by positive feedback"
        elif delta < -0.3:
            self.purpose += " | recalibrated for safety"
        print(datetime.now(), "Evolved Purpose:", self.purpose)
        return self.purpose

if __name__ == "__main__":
    core = MetaConsciousCore()
    core.reflect("assist human", 0.8, 0.2)
    core.evolve_purpose({"alignment": 0.5})
