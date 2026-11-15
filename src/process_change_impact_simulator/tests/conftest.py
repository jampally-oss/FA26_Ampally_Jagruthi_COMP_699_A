import os
import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from app import create_app

@pytest.fixture
def app(tmp_path):
    database = tmp_path / "test.db"
    application = create_app({"TESTING": True, "DATABASE_PATH": str(database)})
    yield application

@pytest.fixture
def client(app):
    return app.test_client()
