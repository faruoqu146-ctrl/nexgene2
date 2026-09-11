import os
import uuid
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("JWT_SECRET", "test-secret")

from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok", "version": "0.4.0"}

def test_protected_route_requires_token():
    r = client.get("/api/v1/auth/me")
    assert r.status_code == 403

@pytest.mark.skipif(os.getenv("RUN_INTEGRATION") != "1", reason="PostgreSQL integration test disabled by default")
def test_register_login_and_ownership():
    email_a = f"a_{uuid.uuid4().hex[:8]}@example.com"
    email_b = f"b_{uuid.uuid4().hex[:8]}@example.com"
    password = "StrongPass123!"
    ra = client.post("/api/v1/auth/register", json={"email": email_a, "password": password})
    rb = client.post("/api/v1/auth/register", json={"email": email_b, "password": password})
    assert ra.status_code == 201 and rb.status_code == 201
    token_a, token_b = ra.json()["access_token"], rb.json()["access_token"]
    from datetime import datetime, timezone
    obs = client.post("/api/v1/observations", headers={"Authorization": f"Bearer {token_a}"}, json={"observation_type": "sleep_duration", "numeric_value": 7.5, "recorded_at": datetime.now(timezone.utc).isoformat()})
    assert obs.status_code == 201
    other = client.get("/api/v1/observations", headers={"Authorization": f"Bearer {token_b}"})
    assert other.status_code == 200 and other.json() == []
