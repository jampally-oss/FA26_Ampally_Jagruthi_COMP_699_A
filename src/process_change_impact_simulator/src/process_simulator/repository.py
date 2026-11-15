from process_simulator.database import connect

def process(path,pid):
 with connect(path) as db:
  r=db.execute('SELECT * FROM processes WHERE id=?',(pid,)).fetchone(); return dict(r) if r else None

def list_processes(path):
 with connect(path) as db: return [dict(r) for r in db.execute('SELECT * FROM processes ORDER BY id DESC')]

def activities(path,pid):
 with connect(path) as db: return [dict(r) for r in db.execute('SELECT * FROM activities WHERE process_id=? ORDER BY id',(pid,))]

def dependencies(path,pid):
 with connect(path) as db: return [dict(r) for r in db.execute('SELECT * FROM dependencies WHERE process_id=? ORDER BY id',(pid,))]

def create_process(path,name,description=''):
 with connect(path) as db: return db.execute('INSERT INTO processes(name,description) VALUES(?,?)',(name,description)).lastrowid

def update_process(path,pid,name,description):
 with connect(path) as db: return db.execute('UPDATE processes SET name=?,description=? WHERE id=?',(name,description,pid)).rowcount

def add_activity(path,pid,name,description='',kind='task',condition=''):
 with connect(path) as db: return db.execute('INSERT INTO activities(process_id,name,description,activity_type,condition_expression) VALUES(?,?,?,?,?)',(pid,name,description,kind,condition)).lastrowid

def update_activity(path,pid,aid,data):
 fields=['name','description','activity_type','condition_expression']; vals=[data.get(k,'') for k in fields]
 with connect(path) as db: return db.execute('UPDATE activities SET name=?,description=?,activity_type=?,condition_expression=? WHERE id=? AND process_id=?',(*vals,aid,pid)).rowcount

def delete_activity(path,pid,aid):
 with connect(path) as db: return db.execute('DELETE FROM activities WHERE id=? AND process_id=?',(aid,pid)).rowcount

def add_dependency(path,pid,a,b,condition=''):
 with connect(path) as db: return db.execute('INSERT INTO dependencies(process_id,predecessor_id,successor_id,condition_expression) VALUES(?,?,?,?)',(pid,a,b,condition)).lastrowid

def delete_dependency(path,pid,did):
 with connect(path) as db: return db.execute('DELETE FROM dependencies WHERE id=? AND process_id=?',(did,pid)).rowcount

def set_endpoints(path,pid,start,end):
 with connect(path) as db: db.execute('UPDATE processes SET start_activity_id=?,end_activity_id=? WHERE id=?',(start,end,pid))

def create_scenario(path,pid,name,description=''):
 with connect(path) as db: return db.execute('INSERT INTO scenarios(process_id,name,description) VALUES(?,?,?)',(pid,name,description)).lastrowid

def scenarios(path,pid):
 with connect(path) as db: return [dict(r) for r in db.execute('SELECT * FROM scenarios WHERE process_id=? ORDER BY id DESC',(pid,))]

def scenario(path,sid):
 with connect(path) as db:
  r=db.execute('SELECT * FROM scenarios WHERE id=?',(sid,)).fetchone()
  if not r:return None
  d=dict(r); d['changes']=[dict(x) for x in db.execute('SELECT * FROM scenario_changes WHERE scenario_id=? ORDER BY id',(sid,))]; return d

def add_scenario_change(path,sid,target_type,target_id,change_type,new_value):
 import json
 with connect(path) as db: return db.execute('INSERT INTO scenario_changes(scenario_id,target_type,target_id,change_type,new_value) VALUES(?,?,?,?,?)',(sid,target_type,target_id,change_type,json.dumps(new_value))).lastrowid

def delete_scenario(path,pid,sid):
 with connect(path) as db: return db.execute('DELETE FROM scenarios WHERE id=? AND process_id=?',(sid,pid)).rowcount

def log_error(path,category,message):
 with connect(path) as db: db.execute('INSERT INTO application_errors(category,message) VALUES(?,?)',(category,message))

def errors(path):
 with connect(path) as db: return [dict(r) for r in db.execute('SELECT * FROM application_errors ORDER BY id DESC LIMIT 100')]
