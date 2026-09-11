FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY tests ./tests

# Render sets $PORT; default to 8000 for local Docker Compose
ENV PORT=8000
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
