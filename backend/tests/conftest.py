import os
import sys
from fastapi.testclient import TestClient
import pytest

# Ensure the backend directory is in the sys.path so 'app' can be imported locally
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app


@pytest.fixture
def app_client():
    """Fixture to provide a FastAPI TestClient instance."""
    with TestClient(app) as client:
        yield client
