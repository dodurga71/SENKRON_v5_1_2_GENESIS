from statistics import fmean
from datetime import datetime

class ConsciousStability:
    def __init__(self):
        self.window = []

    def update(self, metrics: dict) -> float:
        val = 1.0
        penalties = [v for k, v in metrics.items() if isinstance(v, (int, float)) and v < 0.0]
        if penalties:
            val -= min(0.5, abs(fmean(penalties)))
        val = max(0.0, min(1.0, val))
        print(datetime.now(), "CSI Updated:", val)
        return val
