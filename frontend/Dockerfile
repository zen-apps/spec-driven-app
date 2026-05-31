# Frontend image — Streamlit UI.
# Phase 1 skeleton: a minimal placeholder page (real chat UI lands in Phase 4).
FROM python:3.12-slim

WORKDIR /app

# Install pinned dependencies first so this layer caches across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY app.py .

# Streamlit serves on 8501; bind to 0.0.0.0 and run headless so it is reachable
# from the host (published 8501:8501 by docker-compose).
EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address", "0.0.0.0", \
     "--server.port", "8501", \
     "--server.headless", "true"]
