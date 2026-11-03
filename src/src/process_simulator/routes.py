from flask import Blueprint, current_app, request, jsonify, abort
from process_simulator import repository as repo
from process_simulator.graph import graph, check_acyclic, impact
from process_simulator.importer import import_json
import networkx as nx
def register_routes(app):
    bp=Blueprint("api",__name__,url_prefix="/api")
    path=lambda:current_app.config["DATABASE_PATH"]
    @bp.post("/processes")
    def create():
        d=request.get_json(silent=True) or {}; name=d.get("name","")
        if not isinstance(name,str) or not name.strip(): abort(400,description="Process name is required.")
        pid=repo.create_process(path(),name.strip(),d.get("description",""))
        return jsonify(repo.process(path(),pid)),201
    @bp.get("/processes")
    def listing(): return jsonify(repo.list_processes(path()))
    @bp.get("/processes/<int:pid>")
    def detail(pid):
        p=repo.process(path(),pid)
        if not p: abort(404,description="Process not found.")
        p["activities"]=repo.activities(path(),pid); p["dependencies"]=repo.dependencies(path(),pid); return jsonify(p)
    @bp.post("/processes/<int:pid>/activities")
    def activity(pid):
        d=request.get_json(silent=True) or {}; kind=d.get("activity_type","task")
        if not repo.process(path(),pid): abort(404,description="Process not found.")
        if not isinstance(d.get("name"),str) or not d["name"].strip(): abort(400,description="Activity name is required.")
        if kind not in {"task","decision","approval","output"}: abort(400,description="Invalid activity type.")
        aid=repo.add_activity(path(),pid,d["name"].strip(),d.get("description",""),kind)
        return jsonify(next(a for a in repo.activities(path(),pid) if a["id"]==aid)),201
    @bp.post("/processes/<int:pid>/dependencies")
    def dependency(pid):
        d=request.get_json(silent=True) or {}
        try:
            a=int(d["predecessor_id"]); b=int(d["successor_id"])
            g=graph(path(),pid)
            if a not in g or b not in g: raise LookupError("Both activities must exist in this process.")
            if a==b: raise ValueError("An activity cannot depend on itself.")
            g.add_edge(a,b); check_acyclic(g)
            did=repo.add_dependency(path(),pid,a,b)
            return jsonify({"dependency_id":did,"status":"created"}),201
        except LookupError as e: abort(404,description=str(e))
        except (ValueError,KeyError,TypeError) as e: abort(400,description=str(e))
        except Exception as e: abort(409,description=str(e))
    @bp.get("/processes/<int:pid>/activities/<int:aid>/impact")
    def analyze(pid,aid):
        try:return jsonify(impact(path(),pid,aid))
        except LookupError as e:abort(404,description=str(e))
    @bp.post("/import")
    def importer():
        d=request.get_json(silent=True)
        if d is None: abort(400,description="A valid JSON request body is required.")
        try:return jsonify(import_json(path(),d)),201
        except ValueError as e:abort(400,description=str(e))
    app.register_blueprint(bp)
