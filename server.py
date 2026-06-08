from fastapi import FastAPI
from pydantic import BaseModel
from core.law_engine import LawEngine
from core.uptime import UptimeTracker

app = FastAPI(title="Heavenet Law 12 API")
law_engine = LawEngine()
uptime_tracker = UptimeTracker()

class LawCheckRequest(BaseModel):
    action: str
    target: str = ""
    user: str = "@me"

class StakeRequest(BaseModel):
    law: int
    amount: int
    purpose: str = ""

@app.post("/api/v1/law/check")
def law_check(req: LawCheckRequest):
    return law_engine.check_action(req.action, req.target)

@app.post("/api/v1/stake")
def stake(req: StakeRequest):
    return {"tx_id": f"mock_0x{req.law}{req.amount}", "law_active": True, "expires": None}

@app.get("/api/v1/uptime")
def uptime():
    return uptime_tracker.get_status()

@app.post("/api/v1/vault/recover")
def vault_recover():
    return {"status": "delay_started", "cosigns_received": 0, "cancel_command": "heavenet vault cancel-recovery"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7712)