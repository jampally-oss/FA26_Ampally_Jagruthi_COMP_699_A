from process_simulator import repository as repo
from process_simulator.graph import graph, check_acyclic

class DependencyError(ValueError):
    pass

def add_dependency(path, pid, predecessor_id, successor_id):
    if not repo.process(path, pid):
        raise LookupError("Process not found.")
    g = graph(path, pid)
    if predecessor_id not in g or successor_id not in g:
        raise LookupError("Both activities must exist in this process.")
    if predecessor_id == successor_id:
        raise DependencyError("An activity cannot depend on itself.")
    if g.has_edge(predecessor_id, successor_id):
        raise DependencyError("This dependency already exists.")
    g.add_edge(predecessor_id, successor_id)
    try:
        check_acyclic(g)
    except ValueError as exc:
        raise DependencyError(str(exc)) from exc
    did = repo.add_dependency(path, pid, predecessor_id, successor_id)
    return {"dependency_id": did, "status": "created"}
