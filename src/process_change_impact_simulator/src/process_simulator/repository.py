from process_simulator.database import connect
import json

def process(path, pid):
    with connect(path) as db:
        row = db.execute("SELECT * FROM processes WHERE id=?", (pid,)).fetchone()
        return dict(row) if row else None

def list_processes(path):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM processes ORDER BY id DESC")]

def activities(path, pid):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM activities WHERE process_id=? ORDER BY id", (pid,))]

def dependencies(path, pid):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM dependencies WHERE process_id=? ORDER BY id", (pid,))]

def create_process(path, name, description=""):
    with connect(path) as db:
        return db.execute("INSERT INTO processes(name,description) VALUES(?,?)", (name, description)).lastrowid

def update_process(path, pid, name, description):
    with connect(path) as db:
        return db.execute("UPDATE processes SET name=?,description=? WHERE id=?", (name, description, pid)).rowcount

def delete_process(path, pid):
    with connect(path) as db:
        return db.execute("DELETE FROM processes WHERE id=?", (pid,)).rowcount

def add_activity(path, pid, name, description="", kind="task", condition=""):
    with connect(path) as db:
        return db.execute(
            "INSERT INTO activities(process_id,name,description,activity_type,condition_expression) VALUES(?,?,?,?,?)",
            (pid, name, description, kind, condition)
        ).lastrowid

def update_activity(path, pid, aid, data):
    with connect(path) as db:
        return db.execute(
            """UPDATE activities SET name=?,description=?,activity_type=?,condition_expression=?
               WHERE id=? AND process_id=?""",
            (data["name"], data.get("description", ""), data.get("activity_type", "task"),
             data.get("condition_expression", ""), aid, pid)
        ).rowcount

def delete_activity(path, pid, aid):
    with connect(path) as db:
        return db.execute("DELETE FROM activities WHERE id=? AND process_id=?", (aid, pid)).rowcount

def add_dependency(path, pid, a, b, condition=""):
    with connect(path) as db:
        return db.execute(
            "INSERT INTO dependencies(process_id,predecessor_id,successor_id,condition_expression) VALUES(?,?,?,?)",
            (pid, a, b, condition)
        ).lastrowid

def update_dependency(path, pid, did, a, b, condition=""):
    with connect(path) as db:
        return db.execute(
            """UPDATE dependencies SET predecessor_id=?,successor_id=?,condition_expression=?
               WHERE id=? AND process_id=?""", (a, b, condition, did, pid)
        ).rowcount

def delete_dependency(path, pid, did):
    with connect(path) as db:
        return db.execute("DELETE FROM dependencies WHERE id=? AND process_id=?", (did, pid)).rowcount

def set_endpoints(path, pid, start, end):
    with connect(path) as db:
        db.execute("UPDATE processes SET start_activity_id=?,end_activity_id=? WHERE id=?", (start, end, pid))
        db.execute("UPDATE activities SET is_start=0,is_end=0 WHERE process_id=?", (pid,))
        if start is not None:
            db.execute("UPDATE activities SET is_start=1 WHERE id=? AND process_id=?", (start, pid))
        if end is not None:
            db.execute("UPDATE activities SET is_end=1 WHERE id=? AND process_id=?", (end, pid))

def create_scenario(path, pid, name, description=""):
    with connect(path) as db:
        return db.execute("INSERT INTO scenarios(process_id,name,description) VALUES(?,?,?)",
                          (pid, name, description)).lastrowid

def scenarios(path, pid):
    with connect(path) as db:
        rows = [dict(r) for r in db.execute("SELECT * FROM scenarios WHERE process_id=? ORDER BY id DESC", (pid,))]
    for row in rows:
        row["changes"] = scenario(path, row["id"])["changes"]
    return rows

def scenario(path, sid):
    with connect(path) as db:
        row = db.execute("SELECT * FROM scenarios WHERE id=?", (sid,)).fetchone()
        if not row:
            return None
        result = dict(row)
        result["changes"] = [dict(x) for x in db.execute(
            "SELECT * FROM scenario_changes WHERE scenario_id=? ORDER BY id", (sid,))]
        for change in result["changes"]:
            try:
                change["new_value_decoded"] = json.loads(change["new_value"])
            except (TypeError, ValueError):
                change["new_value_decoded"] = change["new_value"]
        return result

def update_scenario(path, pid, sid, name, description):
    with connect(path) as db:
        return db.execute("UPDATE scenarios SET name=?,description=? WHERE id=? AND process_id=?",
                          (name, description, sid, pid)).rowcount

def clear_scenario_changes(path, sid):
    with connect(path) as db:
        db.execute("DELETE FROM scenario_changes WHERE scenario_id=?", (sid,))

def add_scenario_change(path, sid, target_type, target_id, change_type, new_value):
    with connect(path) as db:
        return db.execute(
            "INSERT INTO scenario_changes(scenario_id,target_type,target_id,change_type,new_value) VALUES(?,?,?,?,?)",
            (sid, target_type, target_id, change_type, json.dumps(new_value))
        ).lastrowid

def delete_scenario(path, pid, sid):
    with connect(path) as db:
        return db.execute("DELETE FROM scenarios WHERE id=? AND process_id=?", (sid, pid)).rowcount

def log_error(path, category, message):
    with connect(path) as db:
        db.execute("INSERT INTO application_errors(category,message) VALUES(?,?)", (category, message))

def errors(path):
    with connect(path) as db:
        return [dict(r) for r in db.execute("SELECT * FROM application_errors ORDER BY id DESC LIMIT 200")]

def clear_errors(path):
    with connect(path) as db:
        return db.execute("DELETE FROM application_errors").rowcount
