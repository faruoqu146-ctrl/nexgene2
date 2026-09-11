# NexGene v0.4 Testing

1. Run `docker compose up --build`.
2. Open `http://localhost:8000/docs`.
3. Register two accounts using `POST /api/v1/auth/register`.
4. Use the returned bearer token with Authorize.
5. Call `/api/v1/auth/me`.
6. Create an observation. The request contains no `user_id`.
7. Log in as the second user and list observations.
8. Confirm the second user cannot see the first user's observation.
9. Run `docker compose exec api pytest -q`.

The normal observation API now derives identity entirely from the authenticated token.
