# FA26_Ampally_Jagruthi_COMP_699_A

# Process Change Impact Simulator

## Project Overview

The **Process Change Impact Simulator** is a Python-based web application for examining how a proposed change to a business process may affect connected activities, approvals, and final outputs.

A business process is represented as a directed graph. Activities are the graph nodes, and dependencies between activities are the directed edges. The application can store process information, add activities, connect activities, validate imported process definitions, detect circular dependencies, and identify activities that are downstream from a selected activity.

The project uses synthetic examples, such as a purchase approval workflow. It is intended for academic development and demonstration and does not require confidential business information.

> **Current project status:** The Week 2 implementation provides working Flask API functionality for process creation and listing, activity creation, dependency creation, JSON import and validation, cycle detection, and downstream impact analysis. The browser-based process editor, change-scenario management, full simulation comparison, graph visualization, and reporting features remain planned work.

---

## 1. Project Objectives

The main objectives are to:

- Create and store business process models.
- Add activities to a process and identify their types.
- Define dependencies between activities.
- Represent process activities and dependencies as a directed graph.
- Identify activities directly connected to a selected activity.
- Find all reachable downstream activities.
- Distinguish direct impacts from indirect impacts.
- Detect circular dependencies.
- Import process definitions from JSON.
- Validate process data before saving it.
- Build a foundation for simulating original and modified process paths.
- Present process analysis results in a form that can later be used by a browser interface and reports.

---

## 2. Planned Features

### 2.1 Process management

- Create and view process models.
- Open a saved process and view its activities and dependencies.
- Edit process details.
- Add, edit, and remove activities.
- Define activity types such as task, decision, approval, and output.
- Create, edit, and remove dependencies.
- Define process starting and ending activities.

### 2.2 Process import and validation

- Import a process definition from a JSON document.
- Check required fields and supported activity types.
- Verify that dependency references point to activities in the process.
- Detect circular dependencies.
- Return useful validation messages.
- Export process definitions as JSON.

### 2.3 Change scenario management

- Create a separate change scenario for a selected process.
- Select an activity, decision condition, approval requirement, or dependency to change.
- Record a proposed new value or condition.
- Keep the original process unchanged when a scenario is created.
- View, edit, and delete saved scenarios.
- Run impact analysis for a selected scenario.

### 2.4 Dependency analysis

- Build a directed graph from process activities and dependencies.
- Identify direct downstream activities.
- Identify all reachable downstream activities.
- Separate direct and indirect impacts.
- Identify affected approvals, decisions, and outputs.
- Present affected activities in a readable result.

### 2.5 Process simulation

- Simulate the original process.
- Simulate a modified process scenario.
- Follow process conditions to determine which activities execute.
- Compare original and modified execution paths.
- Identify activities that are skipped or newly required.
- Compare final outputs.

### 2.6 Visualization and reporting

- Display a process dependency graph.
- Highlight affected activities after impact analysis.
- Compare original and modified process paths.
- Present impact summaries for process managers.
- Export analysis results as a report.

### 2.7 Administration

- View stored process models and change scenarios.
- Remove test process data when appropriate.
- Review application errors from validation and simulation operations.
- Display confirmation messages after successful operations.

---

## 3. Functional Requirements

The project has 50 planned functional requirements, grouped into seven areas:

| Group | Requirement IDs | Area |
|---|---|---|
| A | FR-01 to FR-12 | Process Analyst Requirements |
| B | FR-13 to FR-18 | Process Import and Validation Requirements |
| C | FR-19 to FR-25 | Change Scenario Requirements |
| D | FR-26 to FR-32 | Dependency Analysis Requirements |
| E | FR-33 to FR-40 | Process Simulation Requirements |
| F | FR-41 to FR-46 | Visualization and Reporting Requirements |
| G | FR-47 to FR-50 | System Administration Requirements |

### 3.1 Requirements selected for the Week 2 implementation

The following requirements have been selected for the current implementation:

| Requirement | Current implementation |
|---|---|
| FR-01 | Create a process with a name and description. |
| FR-02 | Return a list of saved processes. |
| FR-05 | Add an activity to an existing process. |
| FR-09 | Create a dependency between two activities. |
| FR-13 | Import a process definition through the JSON import API. |
| FR-14 | Validate the JSON structure before saving imported data. |
| FR-15 | Return validation errors for missing or invalid information. |
| FR-17 | Check that dependency references point to existing activities. |
| FR-18 | Detect and reject circular dependencies. |
| FR-26 | Represent process activities and dependencies as a directed graph. |
| FR-27 | Identify direct downstream activities. |
| FR-28 | Identify all reachable downstream activities. |
| FR-30 | Separate direct and indirect downstream activities. |
| FR-32 | Return affected activities in a readable JSON result. |

These are the selected requirements represented in the Week 2 code. The remaining requirements are planned and should not be described as completed until they are implemented and tested.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 (also compatible with supported Python 3.11/3.12 environments) | Main programming language |
| Flask | Web application framework and API endpoints |
| SQLite | Local relational database |
| Python `sqlite3` | Database connections and SQL operations |
| NetworkX | Directed graphs, cycle detection, and downstream analysis |
| HTML and CSS | Planned browser interface |
| JSON | Process import format and API request/response data |
| pytest | Automated testing |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and source-code hosting |

The current implementation uses Python's built-in `sqlite3` module. Flask-SQLAlchemy, Pandas, NumPy, Plotly, and Matplotlib are not required by the current Week 2 source code. Add a package to `requirements.txt` only when the project implementation uses it.

---

## 5. Project Structure

The current Week 2 source structure is:

```text
process_change_impact_simulator_week2/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── instance/
│   └── .gitkeep
│
├── src/
│   └── process_simulator/
│       ├── __init__.py
│       ├── database.py
│       ├── schema.sql
│       ├── repository.py
│       ├── graph.py
│       ├── importer.py
│       └── routes.py
│
├── examples/
│   └── sample_process.json
│
└── tests/
    ├── conftest.py
    └── test_core.py
```

### 5.1 Main files and responsibilities

| File | Responsibility |
|---|---|
| `app.py` | Creates and configures the Flask application, initializes the database, registers routes, and provides the home endpoint. |
| `config.py` | Defines the application configuration and SQLite database path. |
| `requirements.txt` | Lists the Python packages needed by the current implementation. |
| `src/process_simulator/database.py` | Creates SQLite connections and initializes database tables from the schema. |
| `src/process_simulator/schema.sql` | Defines the process, activity, and dependency tables and their relationships. |
| `src/process_simulator/repository.py` | Contains database operations for processes, activities, and dependencies. |
| `src/process_simulator/graph.py` | Builds the directed graph and calculates downstream impacts. |
| `src/process_simulator/importer.py` | Validates JSON process definitions, checks dependency references, detects cycles, and saves valid imports. |
| `src/process_simulator/routes.py` | Defines Flask API endpoints for process operations, activity operations, dependencies, import, and impact analysis. |
| `examples/sample_process.json` | Provides an example process definition for testing JSON import. |
| `tests/conftest.py` | Creates a test application using a temporary SQLite database. |
| `tests/test_core.py` | Contains automated tests for the main Week 2 functionality. |
| `instance/` | Stores the local SQLite database created when the application runs. |

The local database file is generated at runtime and should not be committed to GitHub.

---

## 6. Software Requirements

### 6.1 Hardware and software

- Windows 10 or later, macOS, or Linux.
- Python 3.11 or later. Python 3.13 was used for the current development and test run.
- Visual Studio Code or another Python editor.
- A modern web browser.
- Internet access during initial package installation.

### 6.2 Check Python

On Windows PowerShell:

```powershell
py --list
python --version
```

The current development environment uses Python 3.13.0.

---

## 7. Installation and Setup

### 7.1 Windows PowerShell

1. Clone or download the GitHub repository.
2. Open the project folder in Visual Studio Code.
3. Open a PowerShell terminal in the project root.
4. Create a virtual environment. Use a Python version installed on your computer. For Python 3.13:

```powershell
py -3.13 -m venv .venv
```

5. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current terminal session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

6. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Set the Python source path:

```powershell
$env:PYTHONPATH = "src"
```

8. Start the Flask application:

```powershell
python app.py
```

9. Open the application in a browser:

```text
http://127.0.0.1:5000
```

The home endpoint should return a JSON response identifying the Process Change Impact Simulator and showing its running status.

### 7.2 macOS or Linux

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH=src
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 8. Dependencies

The current `requirements.txt` contains:

```text
Flask==3.1.2
networkx==3.5
pytest==8.4.2
```

Install the packages with:

```powershell
pip install -r requirements.txt
```

SQLite is included with Python, so a separate SQLite package is not needed.

To check installed packages:

```powershell
pip list
```

When adding a new library, update `requirements.txt` and test the installation in a fresh virtual environment.

---

## 9. Database Setup

The application uses SQLite for local data storage. The database is initialized automatically when the Flask application starts.

The database file is created at:

```text
instance/process_simulator.db
```

The schema is defined in:

```text
src/process_simulator/schema.sql
```

### 9.1 Database tables

| Table | Purpose |
|---|---|
| `processes` | Stores process names, descriptions, and creation timestamps. |
| `activities` | Stores activities associated with a process, including their names, descriptions, and types. |
| `dependencies` | Stores directed connections between activities. |

### 9.2 Database relationships

- One process can contain multiple activities.
- One process can contain multiple dependencies.
- Each dependency connects a predecessor activity to a successor activity.
- Foreign keys help maintain relationships between stored records.
- Duplicate dependency pairs are restricted by a database uniqueness constraint.

The database is initialized by `initialize_database()` in `src/process_simulator/database.py`. The application does not require a separate manual database initialization command.

The database file contains local development data. Back up any data you need before deleting it. The `.gitignore` file excludes local database files from Git.

---

## 10. Using the API

The current Week 2 application provides JSON API endpoints. These endpoints can be tested through PowerShell, a REST client, or another HTTP client.

### 10.1 Home endpoint

```http
GET /
```

Returns the application name and running status.

### 10.2 Create a process — FR-01

```http
POST /api/processes
Content-Type: application/json
```

Example request:

```json
{
  "name": "Purchase Approval",
  "description": "Purchase request approval workflow"
}
```

The application returns the saved process details, including its database ID.

### 10.3 List processes — FR-02

```http
GET /api/processes
```

Returns the saved process records.

### 10.4 View one process

```http
GET /api/processes/<process_id>
```

Returns the selected process, its activities, and its dependencies.

### 10.5 Add an activity — FR-05

```http
POST /api/processes/<process_id>/activities
Content-Type: application/json
```

Example request:

```json
{
  "name": "Manager Approval",
  "activity_type": "approval"
}
```

Supported activity types:

- `task`
- `decision`
- `approval`
- `output`

### 10.6 Create a dependency — FR-09

```http
POST /api/processes/<process_id>/dependencies
Content-Type: application/json
```

Example request:

```json
{
  "predecessor_id": 1,
  "successor_id": 2
}
```

The application checks that both activities belong to the selected process and that the new dependency does not create a cycle.

### 10.7 Analyze downstream impact — FR-27, FR-28, FR-30, FR-32

```http
GET /api/processes/<process_id>/activities/<activity_id>/impact
```

The response contains:

- `changed_activity`
- `direct_downstream`
- `indirect_downstream`
- `all_affected`

The direct list contains the immediate successor activities. The indirect list contains reachable downstream activities that are not immediate successors.

### 10.8 Import a process from JSON — FR-13 to FR-18

```http
POST /api/import
Content-Type: application/json
```

Example request:

```json
{
  "process": {
    "name": "Purchase Approval",
    "description": "Example purchase workflow"
  },
  "activities": [
    {
      "key": "submit",
      "name": "Submit Purchase Request",
      "activity_type": "task"
    },
    {
      "key": "manager",
      "name": "Manager Approval",
      "activity_type": "approval"
    },
    {
      "key": "finance",
      "name": "Finance Review",
      "activity_type": "approval"
    },
    {
      "key": "order",
      "name": "Create Purchase Order",
      "activity_type": "output"
    }
  ],
  "dependencies": [
    {"from": "submit", "to": "manager"},
    {"from": "manager", "to": "finance"},
    {"from": "finance", "to": "order"}
  ]
}
```

The `key` value identifies an activity within the JSON document. Dependencies use these keys to identify the activities they connect.

The importer checks the required process information, activity keys, activity names, supported activity types, dependency references, and circular dependencies before saving the process.

A sample import document is available at:

```text
examples/sample_process.json
```

---

## 11. Example Workflow and Impact Analysis

The project uses a synthetic Purchase Approval workflow to demonstrate dependency analysis.

```text
Submit Purchase Request
          |
          v
    Manager Approval
          |
          v
     Finance Review
          |
          v
  Create Purchase Order
```

If `Submit Purchase Request` is selected for impact analysis:

| Result type | Expected activity |
|---|---|
| Direct downstream | Manager Approval |
| Indirect downstream | Finance Review and Create Purchase Order |
| All affected | All three downstream activities |

This example shows how a change to one activity can be traced through the rest of the process.

### 11.1 Manual API test example using PowerShell

After starting the application, open a second PowerShell terminal in the project directory. Activate the virtual environment and set the source path.

Create a process:

```powershell
$process = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes" `
  -ContentType "application/json" `
  -Body '{"name":"Purchase Approval","description":"Purchase request approval workflow"}'

$processId = $process.id
```

Use `$processId` as the variable name. Do not use `$pid`, because PowerShell reserves `$PID` as a read-only variable.

Create activities:

```powershell
$a1 = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/activities" `
  -ContentType "application/json" `
  -Body '{"name":"Submit Purchase Request","activity_type":"task"}'

$a2 = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/activities" `
  -ContentType "application/json" `
  -Body '{"name":"Manager Approval","activity_type":"approval"}'

$a3 = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/activities" `
  -ContentType "application/json" `
  -Body '{"name":"Create Purchase Order","activity_type":"output"}'
```

Create dependencies:

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/dependencies" `
  -ContentType "application/json" `
  -Body "{`"predecessor_id`":$($a1.id),`"successor_id`":$($a2.id)}"

Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/dependencies" `
  -ContentType "application/json" `
  -Body "{`"predecessor_id`":$($a2.id),`"successor_id`":$($a3.id)}"
```

Run impact analysis:

```powershell
Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:5000/api/processes/$processId/activities/$($a1.id)/impact" |
  ConvertTo-Json -Depth 5
```

The expected result identifies Manager Approval as direct downstream and Create Purchase Order as indirect downstream.

---

## 12. Testing

Run automated tests from the project root. Make sure the virtual environment is active and `PYTHONPATH` is set.

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

The Week 2 development test run produced:

```text
....                                                                     [100%]
4 passed in 0.47s
```

### 12.1 Tests included

| Test | Purpose | Observed result |
|---|---|---|
| Process creation, listing, activity creation, and dependency creation | Checks the main process API operations. | Passed |
| Downstream impact | Checks direct and indirect downstream activity identification. | Passed |
| JSON import and validation | Checks valid import and rejection of a missing dependency reference. | Passed |
| Circular dependency validation | Checks rejection of an imported process containing a cycle. | Passed |

### 12.2 Manual testing performed

The application was also tested through PowerShell:

- Created a Purchase Approval process.
- Added Submit Purchase Request, Manager Approval, and Create Purchase Order activities.
- Created two dependencies between the three activities.
- Ran downstream impact analysis.
- Confirmed that Manager Approval appeared in `direct_downstream`.
- Confirmed that Create Purchase Order appeared in `indirect_downstream`.
- Confirmed that both activities appeared in `all_affected`.

The test results above describe the cases that were actually run. Additional testing is required for unimplemented features and for broader input conditions.

---

## 13. Known Limitations and Work Remaining

The current implementation is an API-focused Week 2 foundation. The following features are not yet available in the current source code:

- Editing process names and descriptions.
- Editing and deleting activities.
- Editing and removing dependencies.
- Defining and managing starting and ending activities.
- Exporting process definitions to JSON.
- Creating, editing, and deleting change scenarios.
- Saving proposed changes separately from the original process.
- Running a complete original-versus-modified process simulation.
- Applying general user-defined decision and approval conditions.
- Comparing executed, skipped, newly required, and final-output activities.
- Displaying a visual process graph in the browser.
- Highlighting affected activities on a graph.
- Providing a complete browser-based process editor.
- Exporting impact analysis reports.
- Providing process manager and administrator screens.
- Authentication and role-based access control.
- Broader performance, compatibility, and security testing.

The current graph analysis identifies downstream dependencies. It does not yet simulate every type of business process behavior. Results should be treated as analysis of the supplied process model, not as guaranteed outcomes in a real organization.

---

## 14. Privacy and Security

- Use synthetic process data for development and demonstrations.
- Do not upload confidential business workflows or personal information.
- Do not commit passwords, API keys, tokens, or other credentials.
- Keep virtual environments and local database files out of version control.
- Do not use Flask debug mode for a public or production deployment.
- Add suitable access controls and stronger input handling before any shared deployment.
- Review file upload validation and database handling before using real organizational information.

### 14.1 Suggested `.gitignore`

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

# Local database files
instance/*.db
*.sqlite
*.sqlite3

# Editor and operating system files
.vscode/
.DS_Store
Thumbs.db
```

---

## 15. Git and GitHub Workflow

Commit work regularly so that the repository shows the project's progress. Use meaningful commit messages for each development task.

Check the changed files:

```powershell
git status
```

Stage and commit the Week 2 implementation:

```powershell
git add README.md requirements.txt app.py config.py src examples tests .gitignore
git commit -m "Implement Week 2 process and impact analysis functionality"
```

Push the changes:

```powershell
git push
```

If this is the first push and the remote has not been configured, add the GitHub repository URL and set the branch:

```powershell
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your own GitHub repository.

Before committing, check that local database files, virtual environments, and credentials are not staged.

### 15.1 Week 2 milestone documentation

The Week 2 milestone document should be stored at:

```text
docs/
└── step_2/
    └── week_2/
        ├── core_functionality.pdf
        └── screenshots/
```

The document should identify the selected functional requirements, explain the implementation for each, list the responsible source modules, summarize actual tests and results, describe technical problems, and identify incomplete work.

---

## 16. Development Milestones

The planned development work is:

1. Complete the requirements, architecture, and data design.
2. Set up the Python, Flask, SQLite, and NetworkX project foundation.
3. Implement process creation and activity management.
4. Implement dependency creation, graph construction, and downstream analysis.
5. Add process import validation and cycle detection.
6. Implement change scenario management.
7. Develop original and modified process simulation.
8. Add process graph visualization and result reporting.
9. Test functional and nonfunctional requirements.
10. Correct defects, improve usability, and complete documentation.
11. Prepare the final project demonstration.

The current Week 2 work covers the process and dependency foundation, JSON import validation, and downstream graph analysis. Later milestones will add the remaining features.

