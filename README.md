# NexGene v0.5

Daily NexGene experience milestone:
- authenticated user
- morning check-in
- evening check-in
- chronological timeline
- simple longitudinal baseline insights

## Run
```bash
docker compose up --build
```

API docs: http://localhost:8000/docs

## Test
```bash
docker compose exec api pytest -q
```

This is a development prototype. Do not use real patient, clinical, genetic, or production credentials.
