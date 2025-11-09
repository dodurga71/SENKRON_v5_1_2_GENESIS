import os, json, psutil
from datetime import datetime

class SGIIDashboard:
    def __init__(self, root="."):
        self.root = os.path.abspath(root)
        self.paths = {
            "diag": os.path.join(self.root, "self_diagnostic.json"),
            "evolution": os.path.join(self.root, "logs", "self_evolution.log"),
            "phoenix": os.path.join(self.root, "logs", "phoenix_repair.log"),
            "regen": os.path.join(self.root, "logs", "regeneration.log")
        }

    def collect_system_metrics(self):
        return {
            "time": datetime.utcnow().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "ram_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }

    def safe_json_parse(self, line):
        try:
            return json.loads(line)
        except Exception:
            return {"raw": line.strip()}

    def summarize_logs(self):
        summary = {}
        for name, path in self.paths.items():
            if os.path.exists(path):
                with open(path, "r", encoding="utf8") as f:
                    lines = f.readlines()[-5:]
                summary[name] = [self.safe_json_parse(l) for l in lines if l.strip()]
        return summary

    def render(self):
        print("\n🧭 SENKRON SGII DASHBOARD v6.1\n" + "="*40)
        sys_metrics = self.collect_system_metrics()
        print(f"🧠 CPU: {sys_metrics['cpu_percent']}% | 💾 RAM: {sys_metrics['ram_percent']}% | 📀 Disk: {sys_metrics['disk_percent']}%")
        print(f"🕓 Uptime since: {sys_metrics['boot_time']}\n")

        logs = self.summarize_logs()
        for key, entries in logs.items():
            print(f"📘 {key.upper()} LOG:")
            for e in entries:
                if "raw" in e:
                    print("  •", e["raw"])
                else:
                    print("  •", e)
            print("-"*40)

if __name__ == "__main__":
    dash = SGIIDashboard(root=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    dash.render()
