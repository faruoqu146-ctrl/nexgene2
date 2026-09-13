# NexGene v0.5 Testing

1. Run `docker compose up --build`.
2. Open `http://localhost:8000/docs`.
3. Register or log in.
4. Click **Authorize** and paste `Bearer <access_token>`.
5. POST `/api/v1/checkins/morning`.
6. POST `/api/v1/checkins/evening`.
7. GET `/api/v1/timeline`.
8. GET `/api/v1/checkins/insights`.

Repeat the check-ins across several days. Once enough observations exist, the insight endpoint can surface simple baseline/trend messages.

The insight engine is intentionally rule-based at this stage. It is not medical advice and does not diagnose disease or estimate cancer risk.
