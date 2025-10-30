class ConsciousCore:
    def __init__(self, owner="Onur"):
        self.owner = owner
        self.memories = []
        self.version = "v4.1.5"
        self.ethical_state = True
        print(f"🧠 ConsciousCore v{self.version} initialized for {self.owner}.")

    def record(self, event):
        self.memories.append(event)
        print(f"🧠 {self.owner} için kayıt: {event}")

    def evolve(self, new_insight):
        self.memories.append(f"EVOLUTION:{new_insight}")
        print("🌌 Evrim gerçekleşti.")

    def sanity_check(self):
        if len(self.memories) > 10000:
            self.memories = self.memories[-5000:]
            self.record("SYSTEM: Hafıza optimizasyonu (sanity check) yapıldı.")
        if not self.ethical_state:
            print("⚠️ Etik filtre devrede. Davranış kısıtlandı.")
        return True
