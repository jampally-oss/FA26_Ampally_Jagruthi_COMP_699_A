# FA26_Ampally_Jagruthi_COMP_699_A
# Process Change Impact Simulator

A Python-based web application that helps users examine how a proposed change to a business process may affect connected activities, approvals, and final outputs.

The project represents a workflow as a directed graph. Users can inspect the process, select an activity, trace downstream dependencies, and compare a sample original workflow with a modified scenario. The project uses synthetic examples, such as purchase approval, so it does not require confidential organizational data.

> **Project status:** Preliminary technical proof of concept (PoC). The current prototype demonstrates basic graph analysis, cycle detection, a simple simulation comparison, a Flask interface, and SQLite storage. It is not yet a complete workflow engine.

## 1. Project objectives

- Create and store sample business process models.
- Represent activities as graph nodes and dependencies as directed edges.
- Identify downstream activities connected to a selected activity.
- Detect circular dependencies in a process graph.
- Simulate a simple process under defined conditions.
- Compare original and modified execution paths.
- Display analysis results through a web interface.
- Import and export process definitions using JSON as the project develops.

## 2. Planned features

### Core features
1. Create and view process models.
2. Add, edit, and remove process activities.
3. Define dependencies between activities.
4. Select an activity, approval, condition, or rule for analysis.
5. Identify directly and indirectly affected activities.
6. Detect circular dependencies.
7. Run a basic simulation of an original and modified process.
8. Compare executed, skipped, and newly included activities.
9. Store process data and results in SQLite.
10. Display results in the browser.

### Planned enhancements
- Generalize simulation rules so they are based on each saved workflow rather than fixed sample activity codes.
- Store change scenarios and simulation results as persistent database records.
- Add more sample workflows, including employee onboarding.
- Improve branching and parallel approval support.
- Add more complete JSON validation and import/export.
- Add downloadable analysis reports and more detailed visualizations.

## 3. Technology stack

| Technology | Purpose |
|---|---|
| Python 3.11 or 3.12 | Main programming language |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration and ORM |
| SQLite | Local relational database |
| NetworkX | Directed graphs, downstream tracing, and cycle detection |
| HTML and CSS | Browser interface |
| Pandas and NumPy | Optional support for structured data and calculations as the project expands |
| Plotly and Matplotlib | Planned graph and results visualization |
| JSON | Process import/export format |
| pytest | Automated testing |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and source-code hosting |

The current PoC requirements file includes Flask, Flask-SQLAlchemy, NetworkX, and pytest. Additional libraries should be added to `requirements.txt` only when they are used by the implementation.

## 4. Project structure

The following is the proposed structure for the project. Some folders and modules are planned and may not exist in the current PoC yet.

```text
process-change-impact-simulator/
├── app.py
├── config.py                         # Planned: application configuration
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── process_simulator.db          # Created locally; do not commit runtime DB
│
├── models/                           # Planned: database models
│   ├── __init__.py
│   ├── process.py
│   ├── activity.py
│   ├── dependency.py
│   ├── change_scenario.py
│   └── simulation_result.py
│
├── routes/                           # Planned: Flask route modules
│   ├── __init__.py
│   ├── dashboard.py
│   ├── processes.py
│   ├── analysis.py
│   └── reports.py
│
├── services/
│   ├── __init__.py
│   └── impact.py                     # Current PoC graph and simulation logic
│   # Planned modules:
│   # graph_builder.py
│   # impact_analyzer.py
│   # simulation_engine.py
│   # import_export.py
│
├── templates/
│   ├── base.html
│   └── index.html                    # Current PoC interface
│
├── static/
│   └── style.css
│   # Planned:
│   # js/graph.js
│
├── data/                             # Planned: synthetic workflow JSON files
│   ├── sample_purchase_process.json
│   └── sample_onboarding_process.json
│
└── tests/
    └── test_impact.py                # Current PoC unit tests
    # Planned:
    # test_routes.py
    # test_database.py
    # test_simulation_engine.py
```

**Current PoC files:** `app.py`, `services/impact.py`, `templates/base.html`, `templates/index.html`, `static/style.css`, `tests/test_impact.py`, and `requirements.txt`.

## 5. Requirements

### Software requirements
- Windows 10 or later, macOS, or Linux.
- Python 3.11 or 3.12 recommended.
- Visual Studio Code or another Python editor.
- A modern web browser.
- Internet access during initial package installation.

Check your Python installation:

```bash
python --version
```

On Windows, the Python launcher can also be used:

```powershell
py -0p
```

## 6. Installation and setup

### Windows PowerShell

1. Download or clone the repository.
2. Open the project folder in VS Code.
3. Open a terminal in the project root.
4. Create a virtual environment:

```powershell
py -3.12 -m venv .venv
```

5. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

6. Update pip and install the dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Start the application:

```powershell
python app.py
```

8. Open this address in a browser:

```text
http://127.0.0.1:5000
```

If PowerShell blocks virtual-environment activation, use the environment's Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

## 7. Dependency information

The current `requirements.txt` should contain:

```text
Flask>=3.0,<4.0
Flask-SQLAlchemy>=3.1,<4.0
networkx>=3.2,<4.0
pytest>=8.0,<9.0
```

Install dependencies with:

```bash
pip install -r requirements.txt
```

If a new library is added during development, update `requirements.txt` and test installation in a fresh virtual environment. Do not list a library as a project dependency until the code actually uses it.

## 8. Database initialization

The current proof of concept uses SQLite. When `app.py` starts, it creates the database tables and inserts the sample purchase approval workflow if the database does not already contain a process.

The database file is created in Flask's instance location, commonly:

```text
instance/process_simulator.db
```

The initial data contains a synthetic purchase approval process with activities such as:

- A1 — Submit purchase request
- A2 — Check purchase amount
- A3 — Manager approval
- A4 — Finance approval
- A5 — Create purchase order
- A6 — Notify requester

The current PoC includes a **Reset sample workflow** action. Use it only when you want to replace the stored demonstration process with the original sample. Do not use the reset action if you need to keep locally entered test data.

For a fresh database, stop the application and back up any data you need before deleting the local SQLite file. Restart the application to create the tables and sample workflow again.

## 9. Using the application

1. Start the Flask application.
2. Open `http://127.0.0.1:5000`.
3. Review the sample purchase approval workflow.
4. Select an activity from the analysis list.
5. Enter a purchase amount and an approval threshold.
6. Select **Analyze and compare**.
7. Review the downstream activities and original/modified simulation paths.
8. Use the JSON impact endpoint to inspect analysis data.

Example endpoint:

```text
http://127.0.0.1:5000/api/process/1/impact?activity=A2
```

The endpoint returns JSON containing the process name, selected activity, downstream activity codes, and graph validation status. The process ID may differ if the local database has been changed.

## 10. Testing

Run the automated tests from the project root:

```bash
pytest -q
```

The current tests cover:
- Downstream activity identification.
- Handling of an unknown activity.
- Circular dependency detection.
- Comparison of original and modified execution results.
- Approval behavior for a purchase amount above the configured threshold.

A passing test suite provides evidence for the specific cases tested; it does not prove that every workflow configuration is correct. Add tests when new features are implemented.

### Suggested additional tests
- Process creation and retrieval through Flask.
- Invalid JSON import.
- Dependencies that reference missing activities.
- Branching workflows with multiple paths.
- Original process preservation after a change is proposed.
- Response-time measurements for larger graphs.
- Browser checks for the main user tasks.

## 11. Technical limitations

- The simulation is a preliminary example, not a general-purpose business process execution engine.
- The sample simulation currently uses fixed activity codes for the purchase workflow.
- Advanced branching, parallel execution, loop handling, and arbitrary user-defined rules still require implementation and testing.
- The current data model is a starter design. Change scenarios and simulation results are not yet fully managed as persistent, versioned records.
- Results are based on supplied sample conditions and should be interpreted as possible effects, not guaranteed outcomes in a real organization.
- The prototype is intended for local development and demonstration. It is not configured for production deployment.

## 12. Privacy and security

- Use synthetic process data only; do not upload confidential company workflows or personal information.
- Do not commit passwords, API keys, tokens, credentials, or secret configuration values.
- Do not commit `.env` files containing secrets.
- Keep local databases and virtual environments out of version control.
- Before any shared or production deployment, replace the development secret key, disable Flask debug mode, validate uploads, add suitable access controls, and review security settings.

A suggested `.gitignore` file is:

```gitignore
# Python
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environments
.venv/
venv/

# Local configuration and secrets
.env
.env.*
!.env.example

# Local database and instance data
instance/
*.db
*.sqlite
*.sqlite3

# Editor and operating-system files
.vscode/
.DS_Store
Thumbs.db
```

If the project later requires configuration variables, document their names in an `.env.example` file with placeholder values only. Never put real credentials in that file.

## 13. Git and GitHub workflow

Commit work regularly so the repository shows the project's progress. Use small commits that describe one meaningful change at a time.

Example commands:

```bash
git init
git add README.md requirements.txt app.py services templates static tests .gitignore
git commit -m "Add initial process impact proof of concept"
```

After creating an empty GitHub repository and connecting it as `origin`, push the initial branch:

```bash
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL from your own GitHub account. Do not use the placeholder literally.

Example follow-up commit messages:

```text
Add purchase approval sample workflow
Implement downstream dependency analysis
Add circular dependency validation
Add simulation comparison tests
Improve process results page
Document installation and testing steps
```

Before committing, review staged files:

```bash
git status
git diff --cached
```

Check that `.env`, local databases, virtual environments, and credentials are not included.

## 14. Development milestones

The planned work is:

1. Complete architecture and data design.
2. Demonstrate graph construction and downstream analysis.
3. Implement process and dependency management.
4. Generalize simulation rules for different process models.
5. Integrate analysis, simulation, storage, and visualization.
6. Test functional and nonfunctional requirements.
7. Correct defects and improve usability.
8. Complete documentation and prepare the final demonstration.

## 15. Project outcome

The intended outcome is a working web application that allows users to model a sample business process, propose a change, identify downstream dependencies, and compare original and modified execution paths. The project will be evaluated through automated tests, manual workflow tests, measured response times, and documented screenshots.

---
