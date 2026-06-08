import json
from datetime import datetime

class UptimeTracker:
    def __init__(self, log_path="data/uptime_log.json"):
        self.log_path = log_path
        try:
            with open(log_path) as f:
                self.data = json.load(f)
        except:
            self.data = {"score": 100.0, "last_heartbeat": datetime.utcnow().isoformat()}

    def get_status(self):
        return {
            "current_score": self.data["score"],
            "required": 22,
            "last_heartbeat": self.data["last_heartbeat"],
            "slash_risk": self.data["score"] < 95
        }