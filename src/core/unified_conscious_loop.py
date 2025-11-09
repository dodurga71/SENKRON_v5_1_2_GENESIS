from datetime import datetime
from conscious.meta_conscious_core import MetaConsciousCore
from conscious.empathic_dialogue_engine import EmpathicDialogueEngine
from conscious.purpose_evolver import PurposeEvolver
from conscious.self_learning_agent import SelfLearningAgent
import json, os, random

class UnifiedConsciousLoop:
    """
    SENKRON Unified Conscious Loop (UCL)
    Bilinç, etik, empati, öğrenme ve amaç evrimini döngüsel olarak birleştirir.
    """

    def __init__(self):
        self.meta = MetaConsciousCore()
        self.dialogue = EmpathicDialogueEngine()
        self.purpose = PurposeEvolver()
        self.agent = SelfLearningAgent()
        self.log_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "self_evolution.log"))

    def cycle(self, user_signal: str, topic: str):
        # Duygusal durum ayarı
        self.dialogue.set_mood(user_signal)

        # Bilinçli yansıma
        result = self.meta.reflect(f"analyze {topic}", signal=random.uniform(0.4, 0.9), risk=random.uniform(0.1, 0.4))

        # Amacı geri bildirimle evrimleştir
        alignment = 0.5 if result else -0.2
        self.purpose.evolve({"alignment": alignment})

        # Öğrenme ajanı veri toplasın
        self.agent.collect(topic)

        # Empatik yanıt üret
        response = self.dialogue.respond(f"Reflected on {topic}")

        # Evrim günlüğüne kaydet
        entry = {
            "time": datetime.utcnow().isoformat(),
            "topic": topic,
            "result": result,
            "response": response,
            "alignment": alignment
        }
        with open(self.log_file, "a", encoding="utf8") as f:
            f.write(json.dumps(entry) + "\n")

        print(datetime.now(), "Unified Loop cycle complete.")

if __name__ == "__main__":
    ucl = UnifiedConsciousLoop()
    ucl.cycle("success", "quantum cognition")
