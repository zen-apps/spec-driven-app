# Backend image — FastAPI + LangChain teaching agent (Phase 1).
#
# Built and run for real in Phase 3 (docker-compose). The ./credentials
# service-account JSON is NOT baked into the image; it is mounted at runtime
# and located via the GOOGLE_APPLICATION_CREDENTIALS env var.

FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application package.
COPY app ./app

# Backend listens on 8000.
EXPOSE 8000

# Run the API. Credentials are expected to be mounted at runtime, e.g.:
#   docker run -v ./credentials:/credentials \
#     -e GOOGLE_APPLICATION_CREDENTIALS=/credentials/service-account-key.json ...
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
