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
def do_POST(self):
    if self.path == "/post":
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        identity = get_identity()
        
        content = data.get("content", "").strip()
        recipients = data.get("recipients", [identity["pubkey"]]) # Default: encrypt to self
        
        # Law VI: Encrypt before saving
        if ENCRYPTION_ENABLED:
            encrypted = subprocess.run(
                ["node", "daemon/crypto.js", "encrypt", content] + recipients,
                capture_output=True, text=True
            ).stdout
            content_to_store = encrypted
        else:
            content_to_store = content
        
        post = {
            "id": hashlib.sha256(f"{time.time()}{content}".encode()).hexdigest()[:16],
            "pubkey": identity["pubkey"],
            "author_id": identity["short_id"],
            "rep": identity["rep"],
            "content": content_to_store,
            "encrypted": ENCRYPTION_ENABLED,
            "signature": sign_post(content, HEAVENET_ROOT / ".heavenet" / "id_ed25519"),
            "timestamp": int(time.time())
        }
        #... rest same