from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Heavenet Law 12 API")

class LawCheckRequest(BaseModel):
    action: str
    target: str = ""
    user: str = "@me"

class StakeRequest(BaseModel):
    law: int
    amount: int
    purpose: str = ""

# In-memory mock data
uptime_score = 99.4
last_heartbeat = datetime.utcnow().isoformat() + "Z"

@app.post("/api/v1/law/check")
def law_check(req: LawCheckRequest):
    # Law 7: Note immutability 
    if req.action == "delete_note":
        return {
            "allowed": False,
            "law_violated": 7,
            "reason": "Notes are immutable. Use archive instead.",
            "slash_amount": 500
        }
    return {"allowed": True, "law_violated": None}

@app.post("/api/v1/stake")
def stake(req: StakeRequest):
    return {
        "tx_id": f"mock_0x{req.law}{req.amount}",
        "law_active": True,
        "expires": None
    }

@app.get("/api/v1/uptime")
def uptime():
    return {
        "current_score": uptime_score,
        "required": 22,
        "last_heartbeat": last_heartbeat,
        "slash_risk": uptime_score < 95
    }

@app.post("/api/v1/vault/recover")
def vault_recover():
    return {
        "status": "delay_started",
        "cosigns_received": 0,
        "cancel_command": "heavenet vault cancel-recovery"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7712)