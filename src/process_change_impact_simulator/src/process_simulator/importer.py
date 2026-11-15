import networkx as nx
from process_simulator import repository as repo
from process_simulator.database import connect

def validate(doc):
    errors = []
    if not isinstance(doc, dict):
        return ["JSON root must be an object."]
    process = doc.get("process")
    activities = doc.get("activities")
    dependencies = doc.get("dependencies")
    if not isinstance(process, dict) or not isinstance(process.get("name"), str) or not process["name"].strip():
        errors.append("process.name is required.")
    if not isinstance(activities, list) or not activities:
        errors.append("activities must be a non-empty list.")
    if not isinstance(dependencies, list):
        errors.append("dependencies must be a list.")
    if errors:
        return errors
    keys, graph = set(), nx.DiGraph()
    for i, activity in enumerate(activities):
        if not isinstance(activity, dict) or not isinstance(activity.get("key"), str) or not activity.get("key", "").strip() or not isinstance(activity.get("name"), str) or not activity.get("name", "").strip():
            errors.append(f"activities[{i}] requires key and name.")
            continue
        if activity["key"] in keys:
            errors.append("Duplicate activity key: " + activity["key"])
        keys.add(activity["key"])
        if activity.get("activity_type", "task") not in {"task", "decision", "approval", "output"}:
            errors.append(f"activities[{i}].activity_type is invalid.")
    graph.add_nodes_from(keys)
    for i, dependency in enumerate(dependencies):
        if not isinstance(dependency, dict) or dependency.get("from") not in keys or dependency.get("to") not in keys:
            errors.append(f"dependencies[{i}] must reference existing activity keys.")
        else:
            graph.add_edge(dependency["from"], dependency["to"])
    if not errors and not nx.is_directed_acyclic_graph(graph):
        errors.append("Circular dependencies are not allowed.")
    return errors

def import_json(path, doc):
    errors = validate(doc)
    if errors:
        raise ValueError(" ".join(errors))
    with connect(path) as db:
        cur = db.execute("INSERT INTO processes(name,description) VALUES(?,?)",
                         (doc["process"]["name"].strip(), doc["process"].get("description", "")))
        pid = cur.lastrowid
        keymap = {}
        for activity in doc["activities"]:
            cur = db.execute(
                "INSERT INTO activities(process_id,name,description,activity_type) VALUES(?,?,?,?)",
                (pid, activity["name"].strip(), activity.get("description", ""),
                 activity.get("activity_type", "task"))
            )
            keymap[activity["key"]] = cur.lastrowid
        for dependency in doc["dependencies"]:
            db.execute(
                "INSERT INTO dependencies(process_id,predecessor_id,successor_id) VALUES(?,?,?)",
                (pid, keymap[dependency["from"]], keymap[dependency["to"]])
            )
    return {"process": repo.process(path, pid), "activities": repo.activities(path, pid),
            "dependencies": repo.dependencies(path, pid)}
