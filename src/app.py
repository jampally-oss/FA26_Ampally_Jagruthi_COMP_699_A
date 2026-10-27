from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from services.impact import build_graph, downstream_activities, simulate, compare_runs, validate_graph

app = Flask(__name__)
app.config["SECRET_KEY"] = "replace-this-development-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///process_simulator.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Process(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    activities = db.relationship("Activity", backref="process", cascade="all, delete-orphan")
    dependencies = db.relationship("Dependency", backref="process", cascade="all, delete-orphan")

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey("process.id"), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(160), nullable=False)
    activity_type = db.Column(db.String(30), default="task")
    condition_text = db.Column(db.String(250), default="always")

class Dependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    process_id = db.Column(db.Integer, db.ForeignKey("process.id"), nullable=False)
    source_code = db.Column(db.String(20), nullable=False)
    target_code = db.Column(db.String(20), nullable=False)
    rule = db.Column(db.String(250), default="always")

def seed_sample():
    if Process.query.first():
        return
    p = Process(name="Purchase Approval Workflow",
                description="Synthetic example used to test downstream impact analysis.")
    db.session.add(p)
    db.session.flush()
    activities = [
        Activity(process_id=p.id, code="A1", name="Submit purchase request", activity_type="task"),
        Activity(process_id=p.id, code="A2", name="Check purchase amount", activity_type="decision"),
        Activity(process_id=p.id, code="A3", name="Manager approval", activity_type="approval"),
        Activity(process_id=p.id, code="A4", name="Finance approval", activity_type="approval"),
        Activity(process_id=p.id, code="A5", name="Create purchase order", activity_type="task"),
        Activity(process_id=p.id, code="A6", name="Notify requester", activity_type="output"),
    ]
    db.session.add_all(activities)
    db.session.flush()
    deps = [
        Dependency(process_id=p.id, source_code="A1", target_code="A2"),
        Dependency(process_id=p.id, source_code="A2", target_code="A3", rule="amount > threshold"),
        Dependency(process_id=p.id, source_code="A3", target_code="A4", rule="approved"),
        Dependency(process_id=p.id, source_code="A4", target_code="A5", rule="approved"),
        Dependency(process_id=p.id, source_code="A5", target_code="A6"),
    ]
    db.session.add_all(deps)
    db.session.commit()

def current_process():
    return Process.query.order_by(Process.id).first()

@app.route("/", methods=["GET"])
def index():
    process = current_process()
    if process is None:
        return "No process is available.", 404
    activities = sorted(process.activities, key=lambda a: a.code)
    deps = process.dependencies
    graph = build_graph(
        [{"id": a.code, "name": a.name, "type": a.activity_type} for a in activities],
        [{"source": d.source_code, "target": d.target_code, "rule": d.rule} for d in deps],
    )
    selected = request.args.get("activity", "A2")
    if selected not in graph:
        selected = next(iter(graph.nodes), "")
    affected_codes = set(downstream_activities(graph, selected)) if selected else set()
    amount = float(request.args.get("amount", 1500))
    threshold = float(request.args.get("threshold", 1000))
    original = simulate(graph, amount=amount, threshold=threshold)
    changed = simulate(graph, amount=amount, threshold=threshold, force_manager_approval=True)
    comparison = compare_runs(original, changed)
    return render_template(
        "index.html", process=process, activities=activities, deps=deps,
        selected=selected, affected_codes=affected_codes, amount=amount,
        threshold=threshold, original=original, changed=changed, comparison=comparison,
        graph_valid=validate_graph(graph)
    )

@app.route("/api/process/<int:process_id>/impact", methods=["GET"])
def impact_api(process_id):
    process = Process.query.get_or_404(process_id)
    graph = build_graph(
        [{"id": a.code, "name": a.name, "type": a.activity_type} for a in process.activities],
        [{"source": d.source_code, "target": d.target_code, "rule": d.rule} for d in process.dependencies],
    )
    activity = request.args.get("activity", "")
    if activity not in graph:
        return jsonify({"error": "Unknown activity code."}), 400
    return jsonify({"process": process.name, "changed_activity": activity,
                    "downstream_activities": downstream_activities(graph, activity),
                    "graph_valid": validate_graph(graph)})

@app.route("/reset", methods=["POST"])
def reset_sample():
    for process in Process.query.all():
        db.session.delete(process)
    db.session.commit()
    seed_sample()
    flash("Sample purchase workflow restored.", "success")
    return redirect(url_for("index"))

with app.app_context():
    db.create_all()
    seed_sample()

if __name__ == "__main__":
    app.run(debug=True)
