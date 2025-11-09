from datetime import datetime

class ThalamicGate:
    def __init__(self, sensitivity: float = 0.5):
        self.sensitivity = max(0.0, min(1.0, sensitivity))

    def filter(self, signal_strength: float) -> bool:
        passed = signal_strength >= self.sensitivity
        print(datetime.now(), "ThalamicGate:", signal_strength, "->", passed)
        return passed
