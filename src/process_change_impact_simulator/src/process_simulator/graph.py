import networkx as nx
from process_simulator import repository as repo

def graph(path, pid):
    g = nx.DiGraph()
    for activity in repo.activities(path, pid):
        g.add_node(activity["id"], **activity)
    for dependency in repo.dependencies(path, pid):
        g.add_edge(dependency["predecessor_id"], dependency["successor_id"],
                   condition=dependency.get("condition_expression", ""), dependency_id=dependency["id"])
    return g

def check_acyclic(g):
    if not nx.is_directed_acyclic_graph(g):
        raise ValueError("Circular dependencies are not allowed.")

def impact(path, pid, activity_id):
    g = graph(path, pid)
    if activity_id not in g:
        raise LookupError("Activity not found in this process.")
    direct = set(g.successors(activity_id))
    downstream = set(nx.descendants(g, activity_id))
    indirect = downstream - direct
    activity_map = {a["id"]: a for a in repo.activities(path, pid)}
    affected = [activity_map[i] for i in sorted(downstream)]
    paths = []
    for target in sorted(downstream):
        for node_path in nx.all_simple_paths(g, activity_id, target):
            paths.append([activity_map[node_id] for node_id in node_path])
    return {
        "changed_activity": activity_map[activity_id],
        "direct_downstream": [activity_map[i] for i in sorted(direct)],
        "indirect_downstream": [activity_map[i] for i in sorted(indirect)],
        "all_affected": affected,
        "affected_special_types": [a for a in affected if a["activity_type"] in {"approval", "decision", "output"}],
        "paths": paths
    }
