FROM python:3.12-slim
WORKDIR /app

# When building from the backend/ directory (recommended on Render)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Tests are optional at runtime – only copy if present
COPY tests* ./tests/

ENV PORT=8000
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
