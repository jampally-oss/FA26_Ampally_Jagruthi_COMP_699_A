import sqlite3
from pathlib import Path
def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    db=sqlite3.connect(path); db.row_factory=sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON"); return db
def initialize_database(path):
    schema=Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    with connect(path) as db: db.executescript(schema)
