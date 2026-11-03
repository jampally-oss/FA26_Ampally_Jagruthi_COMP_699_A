from process_simulator.database import connect
def process(path, pid):
    with connect(path) as db:
        r=db.execute("SELECT * FROM processes WHERE id=?",(pid,)).fetchone()
        return dict(r) if r else None
def create_process(path, name, description=""):
    with connect(path) as db:
        cur=db.execute("INSERT INTO processes(name,description) VALUES(?,?)",(name,description)); return cur.lastrowid
def list_processes(path):
    with connect(path) as db: return [dict(r) for r in db.execute("SELECT * FROM processes ORDER BY id")]
def activities(path,pid):
    with connect(path) as db: return [dict(r) for r in db.execute("SELECT * FROM activities WHERE process_id=? ORDER BY id",(pid,))]
def dependencies(path,pid):
    with connect(path) as db: return [dict(r) for r in db.execute("SELECT * FROM dependencies WHERE process_id=?",(pid,))]
def add_activity(path,pid,name,description,kind):
    with connect(path) as db:
        c=db.execute("INSERT INTO activities(process_id,name,description,activity_type) VALUES(?,?,?,?)",(pid,name,description,kind)); return c.lastrowid
def add_dependency(path,pid,a,b):
    with connect(path) as db:
        ids={r[0] for r in db.execute("SELECT id FROM activities WHERE process_id=? AND id IN (?,?)",(pid,a,b))}
        if ids!={a,b}: raise LookupError("Both activities must exist in this process.")
        c=db.execute("INSERT INTO dependencies(process_id,predecessor_id,successor_id) VALUES(?,?,?)",(pid,a,b)); return c.lastrowid
