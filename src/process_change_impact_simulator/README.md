# Process Change Impact Simulator — Week 3 Source Package

This is the application source package for Week 3 integration and initial working-system testing. No Week 3 report is included yet; prepare the report only after the application is run and the test evidence is collected on your computer.

## Stack
- Python 3.13
- Flask 3.1.2
- SQLite (`sqlite3`)
- NetworkX 3.5
- pytest 8.4.2
- HTML/CSS/Jinja2 (no JavaScript)

## Setup (Windows PowerShell)
```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:PYTHONPATH = "src"
python app.py
```
Open http://127.0.0.1:5000. If script activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` and activate again.

## Tests
Open a second PowerShell terminal, activate the same environment, then:
```powershell
$env:PYTHONPATH = "src"
python -m pytest -v
```
Do not write test results into the course report until this command completes locally. If a test fails, save the complete traceback.

## Representative workflow
1. Create a process from the dashboard.
2. Open it and add activities: Submit Request (task), Manager Approval (approval), Create Purchase Order (output).
3. Add dependencies Submit → Approval → Create PO.
4. Analyze downstream impact from Submit. Approval should be direct; Create PO indirect.
5. Create a scenario that skips Manager Approval and compare original and modified execution results.

## API quick reference
- `GET /api/health`
- `POST, GET /api/processes`
- `GET, PATCH /api/processes/<pid>`
- `POST /api/processes/<pid>/activities`
- `PATCH, DELETE /api/processes/<pid>/activities/<aid>`
- `POST /api/processes/<pid>/dependencies`
- `DELETE /api/processes/<pid>/dependencies/<did>`
- `PUT /api/processes/<pid>/endpoints`
- `GET /api/processes/<pid>/activities/<aid>/impact`
- `POST /api/import`, `GET /api/processes/<pid>/export`
- `POST, GET /api/processes/<pid>/scenarios`
- `POST /api/processes/<pid>/simulate`
- `GET /api/processes/<pid>/scenarios/<sid>/compare`
- `DELETE /api/processes/<pid>/scenarios/<sid>`
- `GET /api/admin/errors`

## Requirement implementation boundary
The current milestone prioritizes the process model CRUD, dependency graph, JSON import/export, validation, scenario storage, downstream impact, basic activity-skip simulation, original/modified execution comparison, and browser workflow. Advanced branch-condition semantics, rich interactive graph rendering, full report generation, authentication/role-based administration, and robust simulation of complex parallel/conditional workflows remain partial or future work. The 50 FR IDs and wording remain the project's requirements baseline; do not mark all 50 complete based on this milestone.

## Database
SQLite database is created automatically at `instance/process_simulator.db`. To reset test data, stop the app and delete this file. The schema is intended for a fresh Week 3 database; back up any existing database before replacing it.
