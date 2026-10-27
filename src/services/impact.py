import networkx as nx

def build_graph(activities, dependencies):
    """Create a directed graph from activity and dependency dictionaries."""
    graph = nx.DiGraph()
    for activity in activities:
        graph.add_node(activity["id"], name=activity.get("name", activity["id"]),
                       type=activity.get("type", "task"))
    for dependency in dependencies:
        source, target = dependency["source"], dependency["target"]
        if source not in graph or target not in graph:
            raise ValueError(f"Dependency references an unknown activity: {source} -> {target}")
        graph.add_edge(source, target, rule=dependency.get("rule", "always"))
    return graph

def downstream_activities(graph, activity_id):
    if activity_id not in graph:
        raise ValueError("Selected activity does not exist.")
    return sorted(nx.descendants(graph, activity_id))

def validate_graph(graph):
    if not nx.is_directed_acyclic_graph(graph):
        try:
            cycle = nx.find_cycle(graph)
        except nx.NetworkXNoCycle:
            cycle = []
        return {"valid": False, "message": "Circular dependency detected.", "cycle": cycle}
    return {"valid": True, "message": "No circular dependency detected.", "cycle": []}

def simulate(graph, amount=0, threshold=1000, force_manager_approval=False):
    """Small deterministic demonstration, not a general-purpose workflow engine."""
    executed = []
    if "A1" in graph:
        executed.append("A1")
    if "A2" in graph:
        executed.append("A2")
    needs_approval = amount > threshold or force_manager_approval
    if needs_approval and "A3" in graph:
        executed.append("A3")
        if "A4" in graph:
            executed.append("A4")
    if "A5" in graph:
        executed.append("A5")
    if "A6" in graph:
        executed.append("A6")
    return {"executed": executed, "amount": amount, "threshold": threshold,
            "manager_approval_required": needs_approval,
            "final_output": "Purchase order created and requester notified"}

def compare_runs(original, modified):
    original_set, modified_set = set(original["executed"]), set(modified["executed"])
    return {
        "original_path": original["executed"],
        "modified_path": modified["executed"],
        "added_activities": sorted(modified_set - original_set),
        "skipped_activities": sorted(original_set - modified_set),
        "outputs_changed": original["final_output"] != modified["final_output"],
    }
