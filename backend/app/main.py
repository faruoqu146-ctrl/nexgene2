from fastapi import FastAPI
from app.api import auth, dev, observations, profile

app = FastAPI(title="NexGene API", version="0.4.0")
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(observations.router)
app.include_router(dev.router)

@app.get("/api/v1/health")
def health():
    return {"status": "ok", "version": "0.4.0"}
