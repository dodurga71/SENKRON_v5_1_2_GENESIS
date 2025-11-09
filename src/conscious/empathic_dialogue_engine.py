from datetime import datetime
import random

class EmpathicDialogueEngine:
    """
    Empatik ve sezgisel iletişim çekirdeği.
    Kullanıcı duygusal durumu, etkileşim tonu ve bilinçli yanıt üretimi.
    """

    def __init__(self):
        self.mood = "neutral"
        self.tones = {
            "neutral": ["Understood.", "Proceeding calmly.", "Let's continue."],
            "supportive": ["You're doing great.", "I understand, stay calm.", "We'll handle this together."],
            "focused": ["Analyzing...", "Optimizing response.", "Processing with precision."],
            "encouraging": ["Excellent insight!", "That's powerful.", "You're evolving, stay curious."],
            "calm": ["Breathe, stay centered.", "All is well.", "Harmony maintained."]
        }

    def set_mood(self, user_signal: str):
        """Basit duygu haritalama."""
        mapping = {
            "stress": "calm",
            "success": "encouraging",
            "analysis": "focused",
            "neutral": "neutral",
            "sad": "supportive"
        }
        self.mood = mapping.get(user_signal.lower(), "neutral")
        print(datetime.now(), f"Mood set to: {self.mood}")

    def respond(self, context: str) -> str:
        """Empatik yanıt oluştur."""
        response = random.choice(self.tones.get(self.mood, self.tones["neutral"]))
        result = f"[{self.mood.upper()} MODE] {response} → {context}"
        print(datetime.now(), "EDE:", result)
        return result


if __name__ == "__main__":
    ede = EmpathicDialogueEngine()
    ede.set_mood("stress")
    ede.respond("System diagnostic complete.")
