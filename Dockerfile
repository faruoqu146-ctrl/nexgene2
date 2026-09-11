FROM python:3.12-slim
WORKDIR /app

# Copy from the backend folder (repo root is the build context)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

# Render sets $PORT; default 8000 for local use
ENV PORT=8000
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
