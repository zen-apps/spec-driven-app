# Backend image — FastAPI served by uvicorn.
# Phase 1 skeleton: no LangChain/Gemini yet (those arrive in Phase 2).
FROM python:3.12-slim

WORKDIR /app

# Install pinned dependencies first so this layer caches across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application package.
COPY app ./app

# Container listens on 8000 (published to host 8001 by docker-compose).
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
