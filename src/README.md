# Process Change Impact Simulator — Technical Proof of Concept

## What this prototype demonstrates
- Flask web interface and SQLite persistence for a synthetic purchase approval workflow.
- NetworkX directed graph construction and downstream dependency tracing.
- Detection of circular dependencies.
- A simplified deterministic simulation and comparison of original and modified paths.
- A JSON endpoint for downstream impact results.
- Automated tests for graph analysis and comparison logic.

## Requirements
- Python 3.11 or 3.12 recommended.
- VS Code or another Python editor.

## Windows setup
Open a terminal in this folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

If PowerShell blocks activation, run the app using `.venv\Scripts\python.exe app.py` after installing packages with `.venv\Scripts\python.exe -m pip install -r requirements.txt`.

## Run tests
```powershell
pytest -q
```

## JSON endpoint
Open `/api/process/1/impact?activity=A2` while the app is running.

## Important limitation
This is a starter proof of concept, not a complete workflow engine. The demonstration simulator uses fixed activity codes (A1–A6) for the sample purchase workflow. Before presenting it as a complete system, generalize the simulation rules to use each process's stored conditions and dependencies, add proper scenario/version records, and test branching and parallel paths. The sample data is synthetic and does not represent a real organization's process.
