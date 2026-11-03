# Process Change Impact Simulator — Week 2 Starter

## Selected functional requirements
This code provides an initial implementation for:
- FR-01 create a process; FR-02 list processes.
- FR-05 add activities; FR-09 create dependencies.
- FR-13 import process JSON; FR-14 validate imported data; FR-15 report invalid/missing fields.
- FR-17 validate dependency references; FR-18 detect circular dependencies.
- FR-26 construct a directed dependency graph; FR-27 identify direct downstream activities; FR-28 identify reachable downstream activities; FR-30 distinguish direct/indirect activities; FR-32 return affected activities as a readable JSON list.

These are the selected requirements represented by this starter. Remaining requirements are not yet implemented.

## Structure
`src/process_simulator/` contains database access, SQL schema, repository operations, graph analysis, JSON import validation, and Flask API routes. `tests/` contains automated API tests. `examples/` contains a sample import file.

## Install and run (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python app.py
```
Open http://127.0.0.1:5000.

## Tests
```powershell
$env:PYTHONPATH = "src"
pytest -q
```
Run tests before reporting results in the milestone document. Do not claim a test passed unless you have run it.

## API
- `POST /api/processes` create a process: `{"name":"Purchase Approval","description":"..."}`
- `GET /api/processes` list processes.
- `GET /api/processes/<process_id>` retrieve a process with activities and dependencies.
- `POST /api/processes/<process_id>/activities` add an activity: `{"name":"Manager Review","activity_type":"approval"}`
- `POST /api/processes/<process_id>/dependencies` add a dependency: `{"predecessor_id":1,"successor_id":2}`
- `GET /api/processes/<process_id>/activities/<activity_id>/impact` analyze downstream impact.
- `POST /api/import` import a JSON process definition; see `examples/sample_process.json`.

## Notes and limitations
SQLite database is created automatically in `instance/`. NetworkX represents the directed graph and computes reachability. Cycles are rejected. This is an API-first implementation; it does not yet include a browser workflow editor, change-scenario simulation, visual graph rendering, authentication, report export, or admin screens. Validate all behavior against your actual local run before submitting.
