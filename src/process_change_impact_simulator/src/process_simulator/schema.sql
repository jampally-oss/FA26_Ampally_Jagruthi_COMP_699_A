PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS processes (
 id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL DEFAULT '',
 start_activity_id INTEGER, end_activity_id INTEGER, created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(start_activity_id) REFERENCES activities(id) ON DELETE SET NULL,
 FOREIGN KEY(end_activity_id) REFERENCES activities(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS activities (
 id INTEGER PRIMARY KEY AUTOINCREMENT, process_id INTEGER NOT NULL, name TEXT NOT NULL,
 description TEXT NOT NULL DEFAULT '', activity_type TEXT NOT NULL CHECK(activity_type IN ('task','decision','approval','output')),
 condition_expression TEXT NOT NULL DEFAULT '', is_start INTEGER NOT NULL DEFAULT 0, is_end INTEGER NOT NULL DEFAULT 0,
 FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS dependencies (
 id INTEGER PRIMARY KEY AUTOINCREMENT, process_id INTEGER NOT NULL, predecessor_id INTEGER NOT NULL,
 successor_id INTEGER NOT NULL, condition_expression TEXT NOT NULL DEFAULT '',
 FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE,
 FOREIGN KEY(predecessor_id) REFERENCES activities(id) ON DELETE CASCADE,
 FOREIGN KEY(successor_id) REFERENCES activities(id) ON DELETE CASCADE,
 UNIQUE(process_id, predecessor_id, successor_id), CHECK(predecessor_id<>successor_id)
);
CREATE TABLE IF NOT EXISTS scenarios (
 id INTEGER PRIMARY KEY AUTOINCREMENT, process_id INTEGER NOT NULL, name TEXT NOT NULL,
 description TEXT NOT NULL DEFAULT '', created_at TEXT DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(process_id) REFERENCES processes(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS scenario_changes (
 id INTEGER PRIMARY KEY AUTOINCREMENT, scenario_id INTEGER NOT NULL,
 target_type TEXT NOT NULL CHECK(target_type IN ('activity','dependency')),
 target_id INTEGER NOT NULL, change_type TEXT NOT NULL, new_value TEXT NOT NULL DEFAULT '',
 FOREIGN KEY(scenario_id) REFERENCES scenarios(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS application_errors (
 id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT NOT NULL, message TEXT NOT NULL,
 created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
