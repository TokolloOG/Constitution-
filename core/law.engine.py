import json

class LawEngine:
    def __init__(self, config_path="config/laws.json"):
        with open(config_path) as f:
            self.laws = json.load(f)["laws"]

    def check_action(self, action, target=""):
        # Law 7: Note immutability
        if action == "delete_note" and "notes" in target:
            law = self.laws["7"]
            return {
                "allowed": False,
                "law_violated": 7,
                "reason": law["rule"],
                "slash_amount": law["slash"]
            }
        return {"allowed": True, "law_violated": None}