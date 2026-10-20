import json
from pathlib import Path

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Process Change Impact Simulator",
    page_icon="",
    layout="wide"
)

st.title("Process Change Impact Simulator")
st.write(
    "I use this application to model a business process, select a proposed change, "
    "trace dependent activities, and compare the original process with the changed process."
)

DEFAULT_PROCESS = {
    "process_name": "Purchase Approval Workflow",
    "activities": [
        {"id": "A1", "name": "Submit Purchase Request", "type": "Start", "condition": "always", "output": "Purchase request"},
        {"id": "A2", "name": "Check Purchase Amount", "type": "Activity", "condition": "always", "output": "Amount checked"},
        {"id": "A3", "name": "Manager Approval", "type": "Approval", "condition": "amount > 500", "output": "Manager decision"},
        {"id": "A4", "name": "Finance Approval", "type": "Approval", "condition": "amount > 1000", "output": "Finance decision"},
        {"id": "A5", "name": "Create Purchase Order", "type": "Activity", "condition": "approved", "output": "Purchase order"},
        {"id": "A6", "name": "Notify Requester", "type": "End", "condition": "always", "output": "Notification sent"}
    ],
    "dependencies": [
        {"source": "A1", "target": "A2", "type": "Sequence"},
        {"source": "A2", "target": "A3", "type": "Approval dependency"},
        {"source": "A3", "target": "A4", "type": "Approval dependency"},
        {"source": "A4", "target": "A5", "type": "Approval dependency"},
        {"source": "A5", "target": "A6", "type": "Sequence"}
    ]
}


def load_process(uploaded_file):
    if uploaded_file is None:
        return json.loads(json.dumps(DEFAULT_PROCESS))
    data = json.load(uploaded_file)
    if not isinstance(data, dict) or not isinstance(data.get("activities"), list) or not isinstance(data.get("dependencies"), list):
        raise ValueError("JSON must contain activities and dependencies lists.")
    data.setdefault("process_name", "Imported Process")
    return data


def validate_process(data):
    activities = data["activities"]
    dependencies = data["dependencies"]
    ids = [str(a.get("id", "")).strip() for a in activities]
    if not activities:
        raise ValueError("Add at least one activity.")
    if any(not x for x in ids):
        raise ValueError("Every activity must have an ID.")
    if len(ids) != len(set(ids)):
        raise ValueError("Activity IDs must be unique.")
    known = set(ids)
    for activity in activities:
        if not str(activity.get("name", "")).strip():
            raise ValueError(f"Activity {activity.get('id')} needs a name.")
    for dep in dependencies:
        if dep.get("source") not in known or dep.get("target") not in known:
            raise ValueError("Every dependency must reference existing activity IDs.")
        if dep.get("source") == dep.get("target"):
            raise ValueError("An activity cannot depend directly on itself.")
    graph = nx.DiGraph()
    graph.add_nodes_from(ids)
    graph.add_edges_from((d["source"], d["target"]) for d in dependencies)
    return graph


def evaluate_condition(condition, amount, approved):
    text = str(condition or "always").strip().lower()
    if text in ("", "always", "true", "yes"):
        return True
    if text in ("approved", "approval_required"):
        return approved
    if text in ("not approved", "rejected"):
        return not approved
    normalized = text.replace(",", "")
    import re
    match = re.fullmatch(r"amount\s*(>=|<=|>|<|==|!=)\s*(-?\d+(?:\.\d+)?)", normalized)
    if match:
        operator, value = match.group(1), float(match.group(2))
        return {
            ">": amount > value,
            ">=": amount >= value,
            "<": amount < value,
            "<=": amount <= value,
            "==": amount == value,
            "!=": amount != value
        }[operator]
    return True


def simulate(data, amount, approved, condition_overrides=None):
    condition_overrides = condition_overrides or {}
    activities = data["activities"]
    graph = validate_process(data)
    records = []
    active = set()
    for node in nx.topological_sort(graph):
        activity = next(a for a in activities if str(a["id"]) == node)
        condition = condition_overrides.get(node, activity.get("condition", "always"))
        parents = list(graph.predecessors(node))
        parents_active = all(parent in active for parent in parents)
        condition_passes = evaluate_condition(condition, amount, approved)
        runs = parents_active and condition_passes
        if runs:
            active.add(node)
        records.append({
            "ID": node,
            "Activity": activity.get("name", node),
            "Type": activity.get("type", "Activity"),
            "Condition": condition,
            "Dependencies Met": "Yes" if parents_active else "No",
            "Condition Met": "Yes" if condition_passes else "No",
            "Status": "Runs" if runs else "Skipped",
            "Output": activity.get("output", "")
        })
    return pd.DataFrame(records), graph


def draw_graph(data, graph, affected=None):
    affected = affected or set()
    positions = nx.spring_layout(graph, seed=7)
    edge_x, edge_y = [], []
    for source, target in graph.edges():
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y, mode="lines",
        line=dict(width=1.5, color="#8A94A6"),
        hoverinfo="none"
    ))
    labels = {str(a["id"]): str(a.get("name", a["id"])) for a in data["activities"]}
    node_x, node_y, colors, hover = [], [], [], []
    for node in graph.nodes():
        x, y = positions[node]
        node_x.append(x)
        node_y.append(y)
        colors.append("#F59E0B" if node in affected else "#2563EB")
        hover.append(f"{node}: {labels.get(node, node)}")
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=list(graph.nodes()), textposition="bottom center",
        hovertext=hover, hoverinfo="text",
        marker=dict(size=28, color=colors, line=dict(width=2, color="#FFFFFF"))
    ))
    fig.update_layout(
        height=430, margin=dict(l=20, r=20, t=20, b=30),
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(visible=False), yaxis=dict(visible=False)
    )
    return fig


if "process_data" not in st.session_state:
    st.session_state.process_data = DEFAULT_PROCESS
if "custom_change" not in st.session_state:
    st.session_state.custom_change = None

with st.sidebar:
    st.header("Process Setup")
    uploaded = st.file_uploader("Import process JSON", type=["json"])
    if uploaded is not None:
        try:
            st.session_state.process_data = load_process(uploaded)
            st.success("Process imported.")
        except (ValueError, json.JSONDecodeError) as error:
            st.error(str(error))

    if st.button("Reset to sample process"):
        st.session_state.process_data = json.loads(json.dumps(DEFAULT_PROCESS))
        st.session_state.custom_change = None
        st.rerun()

data = st.session_state.process_data

try:
    graph = validate_process(data)
except (ValueError, nx.NetworkXError) as error:
    st.error(str(error))
    st.stop()

st.subheader(data.get("process_name", "Business Process"))
st.caption("Blue nodes represent process activities. Orange nodes represent activities affected by the selected change.")

with st.expander("Edit process activities", expanded=False):
    activity_df = pd.DataFrame(data["activities"])
    edited_activities = st.data_editor(
        activity_df,
        num_rows="dynamic",
        use_container_width=True,
        key="activities_editor"
    )
    if st.button("Save activity changes"):
        try:
            updated = dict(data)
            updated["activities"] = edited_activities.fillna("").to_dict("records")
            validate_process(updated)
            st.session_state.process_data = updated
            st.success("Activity changes saved.")
            st.rerun()
        except (ValueError, KeyError) as error:
            st.error(str(error))

with st.expander("Edit process dependencies", expanded=False):
    dependency_df = pd.DataFrame(data["dependencies"])
    edited_dependencies = st.data_editor(
        dependency_df,
        num_rows="dynamic",
        use_container_width=True,
        key="dependencies_editor"
    )
    if st.button("Save dependency changes"):
        try:
            updated = dict(data)
            updated["dependencies"] = edited_dependencies.fillna("").to_dict("records")
            validate_process(updated)
            st.session_state.process_data = updated
            st.success("Dependency changes saved.")
            st.rerun()
        except (ValueError, KeyError) as error:
            st.error(str(error))

data = st.session_state.process_data
try:
    graph = validate_process(data)
except (ValueError, nx.NetworkXError) as error:
    st.error(str(error))
    st.stop()

if not nx.is_directed_acyclic_graph(graph):
    st.error("Circular dependency detected. Resolve the cycle before running the simulation.")
    st.write("Activities involved in cycles:", ", ".join(sorted(nx.nodes_with_selfloops(graph))) or "See dependency table for the circular path.")
    try:
        cycle = nx.find_cycle(graph)
        st.write("Example cycle:", " → ".join([edge[0] for edge in cycle] + [cycle[-1][1]]))
    except nx.NetworkXNoCycle:
        pass
    st.stop()

st.header("Run Process Simulation")
left, right = st.columns(2)
with left:
    amount = st.number_input("Purchase amount", min_value=0.0, value=1500.0, step=100.0)
with right:
    approved = st.selectbox("Overall approval outcome", ["Approved", "Not approved"]) == "Approved"

activity_ids = [str(a["id"]) for a in data["activities"]]
activity_names = {str(a["id"]): str(a.get("name", a["id"])) for a in data["activities"]}

with st.form("change_form"):
    st.subheader("Propose a process change")
    selected_id = st.selectbox(
        "Activity, approval, or rule to change",
        activity_ids,
        format_func=lambda value: f"{value} — {activity_names.get(value, value)}"
    )
    change_type = st.selectbox(
        "Change type",
        ["Change condition", "Change dependency"]
    )
    proposed_condition = ""
    dependency_target = ""
    dependency_action = ""
    if change_type == "Change condition":
        current_activity = next(a for a in data["activities"] if str(a["id"]) == selected_id)
        proposed_condition = st.text_input(
            "New condition",
            value=str(current_activity.get("condition", "always")),
            help="Supported examples: always, approved, not approved, amount > 500, amount >= 1000."
        )
    else:
        possible_targets = [node for node in activity_ids if node != selected_id]
        dependency_target = st.selectbox("Connected activity", possible_targets)
        dependency_action = st.selectbox("Dependency action", ["Add dependency", "Remove dependency"])
    submitted = st.form_submit_button("Apply proposed change and compare")

if submitted:
    st.session_state.custom_change = {
        "selected_id": selected_id,
        "change_type": change_type,
        "proposed_condition": proposed_condition,
        "dependency_target": dependency_target,
        "dependency_action": dependency_action
    }

change = st.session_state.custom_change
original_data = json.loads(json.dumps(data))
changed_data = json.loads(json.dumps(data))
changed_node = None
change_message = "No proposed change applied yet."

if change:
    changed_node = change["selected_id"]
    change_message = f"Proposed change selected for {changed_node} — {activity_names.get(changed_node, changed_node)}."
    if change["change_type"] == "Change condition":
        for activity in changed_data["activities"]:
            if str(activity["id"]) == changed_node:
                activity["condition"] = change["proposed_condition"]
        change_message += f" New condition: {change['proposed_condition']}."
    else:
        source = change["selected_id"]
        target = change["dependency_target"]
        edge = next(
            ((d["source"], d["target"]) for d in changed_data["dependencies"]
             if d["source"] == source and d["target"] == target),
            None
        )
        if change["dependency_action"] == "Add dependency":
            if edge is None:
                changed_data["dependencies"].append({
                    "source": source,
                    "target": target,
                    "type": "Proposed dependency"
                })
                change_message += f" Dependency {source} → {target} added."
            else:
                change_message += f" Dependency {source} → {target} already exists."
        else:
            if edge is not None:
                changed_data["dependencies"] = [
                    d for d in changed_data["dependencies"]
                    if not (d["source"] == source and d["target"] == target)
                ]
                change_message += f" Dependency {source} → {target} removed."
            else:
                change_message += f" Dependency {source} → {target} did not exist."

st.info(change_message)

try:
    original_results, original_graph = simulate(original_data, amount, approved)
    changed_results, changed_graph = simulate(changed_data, amount, approved)
    if not nx.is_directed_acyclic_graph(changed_graph):
        st.error("The proposed dependency change creates a circular dependency. The changed process cannot be simulated.")
        st.stop()
except (ValueError, KeyError, nx.NetworkXError) as error:
    st.error(f"Simulation could not run: {error}")
    st.stop()

original_status = original_results.set_index("ID")["Status"].to_dict()
changed_status = changed_results.set_index("ID")["Status"].to_dict()
affected = {
    node for node in set(original_status) | set(changed_status)
    if original_status.get(node) != changed_status.get(node)
}

if change and changed_node:
    try:
        affected.update(nx.descendants(changed_graph, changed_node))
    except nx.NetworkXError:
        pass
    try:
        affected.update(nx.descendants(original_graph, changed_node))
    except nx.NetworkXError:
        pass

st.header("Impact Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Total activities", len(data["activities"]))
m2.metric("Affected downstream activities", len(affected))
m3.metric(
    "Activities with changed run status",
    sum(1 for node in original_status if original_status.get(node) != changed_status.get(node))
)

tab1, tab2, tab3 = st.tabs(["Dependency Graph", "Before and After", "Detailed Results"])

with tab1:
    st.plotly_chart(draw_graph(changed_data, changed_graph, affected), use_container_width=True)
    if affected:
        st.write("Potentially affected activities:")
        st.dataframe(
            pd.DataFrame([
                {"ID": node, "Activity": activity_names.get(node, node)}
                for node in sorted(affected)
            ]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No downstream activities were identified for the current change.")

with tab2:
    comparison = pd.DataFrame({
        "ID": original_results["ID"],
        "Activity": original_results["Activity"],
        "Original Status": original_results["Status"],
        "Changed Status": changed_results["Status"],
        "Original Condition": original_results["Condition"],
        "Changed Condition": changed_results["Condition"],
        "Impact": [
            "Status changed" if original_status.get(node) != changed_status.get(node)
            else ("Potentially affected" if node in affected else "No detected impact")
            for node in original_results["ID"]
        ]
    })
    st.dataframe(comparison, use_container_width=True, hide_index=True)

    status_counts = comparison["Impact"].value_counts().reset_index()
    status_counts.columns = ["Impact", "Activities"]
    fig = go.Figure(go.Bar(
        x=status_counts["Impact"],
        y=status_counts["Activities"],
        marker_color=["#16A34A" if x == "No detected impact" else "#F59E0B" for x in status_counts["Impact"]]
    ))
    fig.update_layout(
        title="Process Change Impact",
        xaxis_title="Impact category",
        yaxis_title="Number of activities",
        height=350
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Original Process Results")
    st.dataframe(original_results, use_container_width=True, hide_index=True)
    st.subheader("Changed Process Results")
    st.dataframe(changed_results, use_container_width=True, hide_index=True)

    st.download_button(
        "Download comparison as CSV",
        data=comparison.to_csv(index=False),
        file_name="process_change_impact.csv",
        mime="text/csv"
    )

st.download_button(
    "Export current process as JSON",
    data=json.dumps(data, indent=2),
    file_name="process_definition.json",
    mime="application/json"
)

st.caption(
    "This proof of concept uses sample process data and rule-based simulation. "
    "Results show possible effects under the entered conditions; they do not guarantee real-world outcomes."
)
