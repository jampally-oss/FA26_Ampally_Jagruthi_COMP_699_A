PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS processes (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
 description TEXT NOT NULL DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS activities (
 id INTEGER PRIMARY KEY AUTOINCREMENT, process_id INTEGER NOT NULL,
 name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '', activity_type TEXT NOT NULL,
 FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE);
CREATE TABLE IF NOT EXISTS dependencies (
 id INTEGER PRIMARY KEY AUTOINCREMENT, process_id INTEGER NOT NULL,
 predecessor_id INTEGER NOT NULL, successor_id INTEGER NOT NULL,
 FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE,
 FOREIGN KEY(predecessor_id) REFERENCES activities(id) ON DELETE CASCADE,
 FOREIGN KEY(successor_id) REFERENCES activities(id) ON DELETE CASCADE,
 UNIQUE(process_id, predecessor_id, successor_id), CHECK(predecessor_id<>successor_id));
