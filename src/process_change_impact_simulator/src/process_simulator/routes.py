import csv
import io
import json
from flask import Blueprint, current_app, request, jsonify, abort, render_template, redirect, url_for, flash, Response
from process_simulator import repository as repo
from process_simulator.process_service import create_process, add_activity
from process_simulator.dependency_service import add_dependency, edit_dependency, DependencyError
from process_simulator.impact_service import analyze_activity_impact
from process_simulator.importer import import_json
from process_simulator.validators import validate_dependency_payload, validate_activity_payload
from process_simulator.exporter import export_process
from process_simulator.simulation_service import simulate, compare
from process_simulator.graph import graph
import networkx as nx

def register_routes(app):
    bp = Blueprint("application", __name__)

    def dbpath():
        return current_app.config["DATABASE_PATH"]

    def body():
        return request.get_json(silent=True) or {}

    def process_or_404(pid):
        item = repo.process(dbpath(), pid)
        if not item:
            abort(404, description="Process not found.")
        return item

    @bp.get("/processes")
    def process_list():
        return render_template("process_list.html", processes=repo.list_processes(dbpath()))

    @bp.post("/processes")
    def process_create_form():
        try:
            item = create_process(dbpath(), request.form.to_dict())
            flash("Process saved.", "success")
            return redirect(url_for("application.process_detail", pid=item["id"]))
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("dashboard"))

    @bp.get("/processes/<int:pid>")
    def process_detail(pid):
        item = process_or_404(pid)
        return render_template("process_detail.html", process=item,
            activities=repo.activities(dbpath(), pid), dependencies=repo.dependencies(dbpath(), pid),
            scenarios=repo.scenarios(dbpath(), pid))

    @bp.post("/processes/<int:pid>/edit")
    def process_edit_form(pid):
        process_or_404(pid)
        try:
            data=request.form.to_dict()
            if not data.get("name","").strip():
                raise ValueError("Process name is required.")
            repo.update_process(dbpath(),pid,data["name"].strip(),data.get("description","").strip())
            flash("Process updated.", "success")
        except ValueError as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/delete")
    def process_delete_form(pid):
        if not repo.delete_process(dbpath(),pid):
            abort(404,description="Process not found.")
        flash("Process deleted.","success")
        return redirect(url_for("application.process_list"))

    @bp.post("/processes/<int:pid>/activities")
    def activity_form(pid):
        try:
            add_activity(dbpath(),pid,request.form.to_dict())
            flash("Activity saved.","success")
        except (ValueError,LookupError) as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/activities/<int:aid>/edit")
    def activity_edit_form(pid,aid):
        process_or_404(pid)
        data=request.form.to_dict()
        errors=validate_activity_payload(data)
        if errors:
            flash(" ".join(errors),"error")
        elif not repo.update_activity(dbpath(),pid,aid,data):
            flash("Activity not found.","error")
        else:
            flash("Activity updated.","success")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/activities/<int:aid>/delete")
    def activity_delete_form(pid,aid):
        if not repo.delete_activity(dbpath(),pid,aid):
            flash("Activity not found.","error")
        else:
            flash("Activity and its connected dependencies deleted.","success")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/dependencies")
    def dependency_form(pid):
        try:
            add_dependency(dbpath(),pid,int(request.form["predecessor_id"]),
                           int(request.form["successor_id"]),request.form.get("condition_expression",""))
            flash("Dependency saved.","success")
        except Exception as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/dependencies/<int:did>/edit")
    def dependency_edit_form(pid,did):
        try:
            edit_dependency(dbpath(),pid,did,int(request.form["predecessor_id"]),
                            int(request.form["successor_id"]),request.form.get("condition_expression",""))
            flash("Dependency updated.","success")
        except Exception as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/dependencies/<int:did>/delete")
    def dependency_delete_form(pid,did):
        if not repo.delete_dependency(dbpath(),pid,did):
            flash("Dependency not found.","error")
        else:
            flash("Dependency removed.","success")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/endpoints")
    def endpoints_form(pid):
        process_or_404(pid)
        start=request.form.get("start_activity_id") or None
        end=request.form.get("end_activity_id") or None
        ids={a["id"] for a in repo.activities(dbpath(),pid)}
        try:
            start=int(start) if start else None
            end=int(end) if end else None
            if (start is not None and start not in ids) or (end is not None and end not in ids):
                raise ValueError("Choose activities from this process.")
            repo.set_endpoints(dbpath(),pid,start,end)
            flash("Process start and end activities saved.","success")
        except ValueError as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.get("/processes/<int:pid>/impact/<int:aid>")
    def impact_page(pid,aid):
        try:
            result=analyze_activity_impact(dbpath(),pid,aid)
        except LookupError as exc:
            abort(404,description=str(exc))
        return render_template("impact_results.html",process=process_or_404(pid),result=result)

    @bp.get("/processes/<int:pid>/graph")
    def graph_page(pid):
        process=process_or_404(pid)
        g=graph(dbpath(),pid)
        if not nx.is_directed_acyclic_graph(g):
            abort(409,description="The process graph contains a cycle.")
        levels={}
        for node in nx.topological_sort(g):
            levels[node]=0 if g.in_degree(node)==0 else 1+max(levels[p] for p in g.predecessors(node))
        grouped={}
        for node,level in levels.items():
            grouped.setdefault(level,[]).append(g.nodes[node])
        max_rows=max((len(v) for v in grouped.values()),default=1)
        max_cols=max(len(grouped),1)
        width=max(700,max_cols*240)
        height=max(220,max_rows*115+80)
        positions={}
        for level,nodes in grouped.items():
            for idx,node in enumerate(nodes):
                positions[node["id"]]=(100+level*220, 65+idx*105)
        edges=[]
        for source,target in g.edges():
            x1,y1=positions[source];x2,y2=positions[target]
            edges.append({"x1":x1+75,"y1":y1,"x2":x2-75,"y2":y2})
        nodes=[]
        for node_id,data in g.nodes(data=True):
            x,y=positions[node_id]
            nodes.append({"id":node_id,"name":data["name"],"kind":data["activity_type"],"x":x,"y":y})
        return render_template("graph.html",process=process,nodes=nodes,edges=edges,width=width,height=height)

    @bp.post("/processes/<int:pid>/scenarios")
    def scenario_form(pid):
        try:
            process_or_404(pid)
            name=request.form.get("name","").strip()
            target_type=request.form.get("target_type","activity")
            target_id=int(request.form.get("target_id","0"))
            change_type=request.form.get("change_type","skip")
            raw=request.form.get("new_value","true")
            value=json.loads(raw) if raw.strip().startswith(("{","[")) else raw
            if not name:
                raise ValueError("Scenario name is required.")
            if target_type=="activity":
                if target_id not in {a["id"] for a in repo.activities(dbpath(),pid)}:
                    raise ValueError("Select an activity from this process.")
                allowed={"skip","rename","condition"}
            elif target_type=="dependency":
                allowed={"remove","condition","add"}
                if target_id not in {d["id"] for d in repo.dependencies(dbpath(),pid)} and not (request.form.get("change_type")=="add" and target_id==0):
                    raise ValueError("Select a dependency from this process, or use ID 0 to add a new dependency.")
            else:
                raise ValueError("Invalid scenario target.")
            if change_type not in allowed:
                raise ValueError("Invalid change type for the selected target.")
            sid=repo.create_scenario(dbpath(),pid,name,request.form.get("description",""))
            repo.add_scenario_change(dbpath(),sid,target_type,target_id,change_type,value)
            flash("Scenario saved separately from the original process.","success")
        except Exception as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/scenarios/<int:sid>/edit")
    def scenario_edit_form(pid,sid):
        data=request.form.to_dict()
        target_type=data.get("target_type","activity")
        try:
            target_id=int(data.get("target_id","0"))
            if target_type=="activity":
                valid_ids={a["id"] for a in repo.activities(dbpath(),pid)}
                allowed={"skip","rename","condition"}
            elif target_type=="dependency":
                valid_ids={d["id"] for d in repo.dependencies(dbpath(),pid)}
                allowed={"remove","condition","add"}
            else:
                raise ValueError("Invalid scenario target.")
            change_type=data.get("change_type","skip")
            valid_add = target_type=="dependency" and change_type=="add" and target_id==0
            if (target_id not in valid_ids and not valid_add) or change_type not in allowed:
                raise ValueError("Choose a valid target and change type. Use target ID 0 to add a dependency.")
            raw=data.get("new_value","true")
            value=json.loads(raw) if raw.strip().startswith(("{","[")) else raw
            if not repo.update_scenario(dbpath(),pid,sid,data.get("name","").strip(),
                                        data.get("description","").strip()):
                raise ValueError("Scenario not found or name is missing.")
            repo.clear_scenario_changes(dbpath(),sid)
            repo.add_scenario_change(dbpath(),sid,target_type,target_id,change_type,value)
            flash("Scenario and its proposed change updated.","success")
        except Exception as exc:
            flash(str(exc),"error")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.post("/processes/<int:pid>/scenarios/<int:sid>/delete")
    def scenario_delete_form(pid,sid):
        if not repo.delete_scenario(dbpath(),pid,sid):
            flash("Scenario not found.","error")
        else:
            flash("Scenario deleted.","success")
        return redirect(url_for("application.process_detail",pid=pid))

    @bp.get("/processes/<int:pid>/scenarios/<int:sid>/compare")
    def scenario_compare_page(pid,sid):
        try:
            result=compare(dbpath(),pid,sid)
        except (ValueError,LookupError) as exc:
            abort(400,description=str(exc))
        return render_template("comparison.html",process=process_or_404(pid),result=result)

    @bp.get("/processes/<int:pid>/report.csv")
    def impact_report(pid):
        process=process_or_404(pid)
        activities=repo.activities(dbpath(),pid)
        output=io.StringIO()
        writer=csv.writer(output)
        writer.writerow(["Process","Activity ID","Activity","Type","Direct downstream","Indirect downstream"])
        for activity in activities:
            result=analyze_activity_impact(dbpath(),pid,activity["id"])
            writer.writerow([process["name"],activity["id"],activity["name"],activity["activity_type"],
                "; ".join(a["name"] for a in result["direct_downstream"]),
                "; ".join(a["name"] for a in result["indirect_downstream"])])
        return Response(output.getvalue(),mimetype="text/csv",
            headers={"Content-Disposition":f'attachment; filename="process_{pid}_impact_report.csv"'})

    @bp.get("/admin")
    def admin_page():
        return render_template("admin.html",processes=repo.list_processes(dbpath()),errors=repo.errors(dbpath()))

    @bp.post("/admin/errors/clear")
    def admin_clear_errors():
        repo.clear_errors(dbpath())
        flash("Error log cleared.","success")
        return redirect(url_for("application.admin_page"))

    @bp.get("/api/health")
    def health():
        return jsonify({"status":"ok","application":"Process Change Impact Simulator"})

    @bp.post("/api/processes")
    def api_create_process():
        try:
            item=create_process(dbpath(),body())
            return jsonify(item),201
        except ValueError as exc:
            abort(400,description=str(exc))

    @bp.get("/api/processes")
    def api_list_processes():
        return jsonify(repo.list_processes(dbpath()))

    @bp.get("/api/processes/<int:pid>")
    def api_detail(pid):
        item=process_or_404(pid)
        item["activities"]=repo.activities(dbpath(),pid)
        item["dependencies"]=repo.dependencies(dbpath(),pid)
        return jsonify(item)

    @bp.patch("/api/processes/<int:pid>")
    def api_update_process(pid):
        data=body()
        if not data.get("name","").strip():
            abort(400,description="Process name is required.")
        if not repo.update_process(dbpath(),pid,data["name"].strip(),data.get("description","").strip()):
            abort(404,description="Process not found.")
        return jsonify(repo.process(dbpath(),pid))

    @bp.delete("/api/processes/<int:pid>")
    def api_delete_process(pid):
        if not repo.delete_process(dbpath(),pid):
            abort(404,description="Process not found.")
        return jsonify({"deleted":True})

    @bp.post("/api/processes/<int:pid>/activities")
    def api_add_activity(pid):
        try:
            return jsonify(add_activity(dbpath(),pid,body())),201
        except LookupError as exc:
            abort(404,description=str(exc))
        except ValueError as exc:
            abort(400,description=str(exc))

    @bp.patch("/api/processes/<int:pid>/activities/<int:aid>")
    def api_edit_activity(pid,aid):
        data=body()
        errors=validate_activity_payload(data)
        if errors:
            abort(400,description=" ".join(errors))
        if not repo.update_activity(dbpath(),pid,aid,data):
            abort(404,description="Activity not found.")
        return jsonify(next(a for a in repo.activities(dbpath(),pid) if a["id"]==aid))

    @bp.delete("/api/processes/<int:pid>/activities/<int:aid>")
    def api_delete_activity(pid,aid):
        if not repo.delete_activity(dbpath(),pid,aid):
            abort(404,description="Activity not found.")
        return jsonify({"deleted":True})

    @bp.post("/api/processes/<int:pid>/dependencies")
    def api_add_dependency(pid):
        data=body()
        errors=validate_dependency_payload(data)
        if errors:
            abort(400,description=" ".join(errors))
        try:
            return jsonify(add_dependency(dbpath(),pid,int(data["predecessor_id"]),
                int(data["successor_id"]),data.get("condition_expression",""))),201
        except LookupError as exc:
            abort(404,description=str(exc))
        except DependencyError as exc:
            abort(409,description=str(exc))

    @bp.patch("/api/processes/<int:pid>/dependencies/<int:did>")
    def api_edit_dependency(pid,did):
        data=body()
        try:
            result=edit_dependency(dbpath(),pid,did,int(data["predecessor_id"]),
                int(data["successor_id"]),data.get("condition_expression",""))
            return jsonify(result)
        except (KeyError,TypeError,ValueError) as exc:
            abort(400,description=str(exc))
        except LookupError as exc:
            abort(404,description=str(exc))
        except DependencyError as exc:
            abort(409,description=str(exc))

    @bp.delete("/api/processes/<int:pid>/dependencies/<int:did>")
    def api_delete_dependency(pid,did):
        if not repo.delete_dependency(dbpath(),pid,did):
            abort(404,description="Dependency not found.")
        return jsonify({"deleted":True})

    @bp.put("/api/processes/<int:pid>/endpoints")
    def api_endpoints(pid):
        data=body()
        ids={a["id"] for a in repo.activities(dbpath(),pid)}
        start=data.get("start_activity_id"); end=data.get("end_activity_id")
        if (start is not None and start not in ids) or (end is not None and end not in ids):
            abort(400,description="Start and end activities must belong to this process.")
        repo.set_endpoints(dbpath(),pid,start,end)
        return jsonify(repo.process(dbpath(),pid))

    @bp.get("/api/processes/<int:pid>/activities/<int:aid>/impact")
    def api_impact(pid,aid):
        try:
            return jsonify(analyze_activity_impact(dbpath(),pid,aid))
        except LookupError as exc:
            abort(404,description=str(exc))

    @bp.post("/api/import")
    def api_import():
        try:
            return jsonify(import_json(dbpath(),body())),201
        except ValueError as exc:
            repo.log_error(dbpath(),"import_validation",str(exc))
            abort(400,description=str(exc))

    @bp.get("/api/processes/<int:pid>/export")
    def api_export(pid):
        try:
            return jsonify(export_process(dbpath(),pid))
        except LookupError as exc:
            abort(404,description=str(exc))

    @bp.post("/api/processes/<int:pid>/scenarios")
    def api_scenario(pid):
        data=body()
        if not data.get("name","").strip():
            abort(400,description="Scenario name is required.")
        if not repo.process(dbpath(),pid):
            abort(404,description="Process not found.")
        changes=data.get("changes",[])
        if not isinstance(changes,list):
            abort(400,description="changes must be a list.")
        valid_targets={"activity","dependency"}
        sid=repo.create_scenario(dbpath(),pid,data["name"].strip(),data.get("description",""))
        try:
            for change in changes:
                target_type=change["target_type"]
                target_id=int(change["target_id"])
                change_type=change["change_type"]
                if target_type not in valid_targets:
                    raise ValueError("Invalid scenario target type.")
                allowed = {"activity":{"skip","rename","condition"},
                           "dependency":{"remove","condition","add"}}
                if change_type not in allowed[target_type]:
                    raise ValueError("Invalid change type for scenario target.")
                valid_ids={a["id"] for a in (repo.activities(dbpath(),pid) if target_type=="activity" else repo.dependencies(dbpath(),pid))}
                valid_add = target_type=="dependency" and change_type=="add" and target_id==0
                if target_id not in valid_ids and not valid_add:
                    raise ValueError("Scenario target does not exist in this process. Use target_id 0 for a new dependency.")
                repo.add_scenario_change(dbpath(),sid,target_type,target_id,change_type,change.get("new_value",True))
        except Exception as exc:
            repo.delete_scenario(dbpath(),pid,sid)
            abort(400,description=f"Invalid scenario change: {exc}")
        return jsonify(repo.scenario(dbpath(),sid)),201

    @bp.get("/api/processes/<int:pid>/scenarios")
    def api_scenarios(pid):
        process_or_404(pid)
        return jsonify(repo.scenarios(dbpath(),pid))

    @bp.patch("/api/processes/<int:pid>/scenarios/<int:sid>")
    def api_update_scenario(pid,sid):
        data=body()
        if not data.get("name","").strip():
            abort(400,description="Scenario name is required.")
        if not repo.update_scenario(dbpath(),pid,sid,data["name"].strip(),data.get("description","")):
            abort(404,description="Scenario not found.")
        return jsonify(repo.scenario(dbpath(),sid))

    @bp.delete("/api/processes/<int:pid>/scenarios/<int:sid>")
    def api_delete_scenario(pid,sid):
        if not repo.delete_scenario(dbpath(),pid,sid):
            abort(404,description="Scenario not found.")
        return jsonify({"deleted":True})

    @bp.post("/api/processes/<int:pid>/simulate")
    def api_simulate(pid):
        try:
            return jsonify(simulate(dbpath(),pid,body().get("scenario_id")))
        except (ValueError,LookupError) as exc:
            abort(400,description=str(exc))

    @bp.get("/api/processes/<int:pid>/scenarios/<int:sid>/compare")
    def api_compare(pid,sid):
        try:
            return jsonify(compare(dbpath(),pid,sid))
        except (ValueError,LookupError) as exc:
            abort(400,description=str(exc))

    @bp.get("/api/admin/errors")
    def api_admin_errors():
        return jsonify(repo.errors(dbpath()))

    app.register_blueprint(bp)
