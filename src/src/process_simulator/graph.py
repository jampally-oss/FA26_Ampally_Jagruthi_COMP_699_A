import networkx as nx
from process_simulator import repository as repo
def graph(path,pid):
    g=nx.DiGraph()
    for a in repo.activities(path,pid): g.add_node(a["id"],**a)
    for d in repo.dependencies(path,pid): g.add_edge(d["predecessor_id"],d["successor_id"])
    return g
def impact(path,pid,aid):
    g=graph(path,pid)
    if aid not in g: raise LookupError("Activity not found in this process.")
    direct=set(g.successors(aid)); all_down=set(nx.descendants(g,aid)); indirect=all_down-direct
    items={a["id"]:a for a in repo.activities(path,pid)}
    return {"changed_activity":items[aid],"direct_downstream":[items[x] for x in sorted(direct)],
            "indirect_downstream":[items[x] for x in sorted(indirect)],
            "all_affected":[items[x] for x in sorted(all_down)]}
def check_acyclic(g):
    if not nx.is_directed_acyclic_graph(g): raise ValueError("Circular dependencies are not allowed.")
