import networkx as nx
from process_simulator import repository as repo
from process_simulator.database import connect
def validate(doc):
    errors=[]
    if not isinstance(doc,dict): return ["JSON root must be an object."]
    p=doc.get("process"); acts=doc.get("activities"); deps=doc.get("dependencies")
    if not isinstance(p,dict) or not isinstance(p.get("name"),str) or not p["name"].strip(): errors.append("process.name is required.")
    if not isinstance(acts,list) or not acts: errors.append("activities must be a non-empty list.")
    if not isinstance(deps,list): errors.append("dependencies must be a list.")
    if errors:return errors
    keys=set(); g=nx.DiGraph()
    for i,a in enumerate(acts):
        if not isinstance(a,dict) or not isinstance(a.get("key"),str) or not a.get("key","").strip() or not isinstance(a.get("name"),str) or not a.get("name","").strip():
            errors.append(f"activities[{i}] requires key and name."); continue
        if a["key"] in keys: errors.append("Duplicate activity key: "+a["key"])
        keys.add(a["key"])
        if a.get("activity_type","task") not in {"task","decision","approval","output"}: errors.append(f"activities[{i}].activity_type is invalid.")
    g.add_nodes_from(keys)
    for i,d in enumerate(deps):
        if not isinstance(d,dict) or d.get("from") not in keys or d.get("to") not in keys: errors.append(f"dependencies[{i}] must reference existing activity keys.")
        else:g.add_edge(d["from"],d["to"])
    if not errors and not nx.is_directed_acyclic_graph(g): errors.append("Circular dependencies are not allowed.")
    return errors
def import_json(path,doc):
    errors=validate(doc)
    if errors: raise ValueError(" ".join(errors))
    pid=repo.create_process(path,doc["process"]["name"],doc["process"].get("description",""))
    keymap={}
    try:
        for a in doc["activities"]: keymap[a["key"]]=repo.add_activity(path,pid,a["name"],a.get("description",""),a.get("activity_type","task"))
        for d in doc["dependencies"]: repo.add_dependency(path,pid,keymap[d["from"]],keymap[d["to"]])
    except Exception:
        with connect(path) as db: db.execute("DELETE FROM processes WHERE id=?",(pid,))
        raise
    return {"process":repo.process(path,pid),"activities":repo.activities(path,pid),"dependencies":repo.dependencies(path,pid)}
