# Frontend image — Streamlit chat UI (Phase 2).
#
# This phase only requires the image to BUILD. Wiring the service into
# docker-compose and pointing it at the backend by compose service name
# (http://backend:8000) is Phase 3. For local runs the app targets the backend
# at http://localhost:8001 (see BACKEND_URL in app.py).

FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application.
COPY app.py ./

# Streamlit's default port.
EXPOSE 8501

# Bind to 0.0.0.0 so the server is reachable from outside the container.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
