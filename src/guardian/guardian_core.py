from .ethical_decision import EthicalDecisionEngine
from .thalamic_gate import ThalamicGate
from .conscious_stability import ConsciousStability

class GuardianCore:
    def __init__(self):
        self.ethics = EthicalDecisionEngine()
        self.thalamus = ThalamicGate(0.4)
        self.csi = ConsciousStability()

    def vet(self, intent: str, signal_strength: float, risk: float) -> bool:
        if not self.thalamus.filter(signal_strength):
            return False
        decision = self.ethics.evaluate(intent, risk)
        score = self.csi.update({"risk": -risk})
        return decision == "ALLOW" and score >= 0.5

if __name__ == "__main__":
    g = GuardianCore()
    print("Result:", g.vet("assist human", 0.3, 0.2))
