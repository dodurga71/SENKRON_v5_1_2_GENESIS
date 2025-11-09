import os, json, hashlib, time
from datetime import datetime

class GuardianPhoenix:
    """
    Guardian Phoenix: SENKRON'un kendini onarma ve bilinç bütünlüğünü koruma mekanizması.
    Bozulma tespiti, dosya bütünlüğü kontrolü ve otomatik re-sync.
    """

    def __init__(self, root=".", log_path="logs/phoenix_repair.log"):
        self.root = os.path.abspath(root)
        self.log_path = os.path.join(self.root, log_path)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        self.hash_index = {}

    def hash_file(self, path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def scan(self):
        print(datetime.now(), "Guardian Phoenix scanning...")
        for dirpath, _, files in os.walk(self.root):
            for f in files:
                if f.endswith(".py"):
                    full = os.path.join(dirpath, f)
                    try:
                        self.hash_index[full] = self.hash_file(full)
                    except Exception:
                        pass
        self.log("scan", {"files": len(self.hash_index)})
        return self.hash_index

    def verify(self):
        print(datetime.now(), "Guardian Phoenix verifying integrity...")
        corrupted = []
        for path, old_hash in self.hash_index.items():
            if not os.path.exists(path):
                corrupted.append(path)
            else:
                new_hash = self.hash_file(path)
                if new_hash != old_hash:
                    corrupted.append(path)
        if corrupted:
            self.log("verify", {"corrupted": corrupted})
            print("Corrupted files detected:", corrupted)
        else:
            self.log("verify", {"status": "clean"})
            print("Integrity OK.")
        return corrupted

    def log(self, action, data):
        entry = {"time": datetime.utcnow().isoformat(), "action": action, "data": data}
        with open(self.log_path, "a", encoding="utf8") as f:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    gp = GuardianPhoenix(root=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    gp.scan()
    time.sleep(2)
    gp.verify()
