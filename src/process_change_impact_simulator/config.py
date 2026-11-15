import os
from pathlib import Path

class Config:
    ROOT = Path(__file__).resolve().parent
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", str(ROOT / "instance" / "process_simulator.db")
    )
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-before-deployment")
