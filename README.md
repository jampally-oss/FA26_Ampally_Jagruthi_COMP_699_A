# Process Change Impact Simulator

## Project Overview

The **Process Change Impact Simulator** is a Python-based web application that helps users understand how a change to a business process can affect other activities, approvals, and final outputs.

The application represents a business process as a directed graph. Activities are the nodes, and dependencies are the connections between them. Users can create processes, add activities, connect activities, analyze downstream impacts, create change scenarios, and compare the original process with a modified version.

The project uses sample business workflows, such as a purchase approval process. It is intended for academic development and demonstration. Use sample data rather than confidential business information.

## Project Objectives

- Create and store business process models.
- Add activities such as tasks, decisions, approvals, and outputs.
- Connect activities using dependencies.
- Identify activities directly and indirectly affected by a change.
- Validate process information and detect circular dependencies.
- Import and export process definitions using JSON.
- Create and save change scenarios without changing the original process.
- Simulate the original and modified process.
- Compare activities and outputs from both simulations.
- Present process information through a browser interface.
- Provide a foundation for future graph visualization and reporting.

## Main Features

### 1. Process Management
- Create a process with a name and description.
- View saved processes.
- Open a process and view its activities and dependencies.
- Add activities to a process.
- Support task, decision, approval, and output activity types.
- Store process information in an SQLite database.

### 2. Process Import, Export, and Validation
- Import process definitions from JSON.
- Check required fields and activity types.
- Check that dependency references point to existing activities.
- Detect circular dependencies.
- Export a saved process as JSON.

### 3. Change Scenario Management
- Create a change scenario for a selected process.
- Select an activity to change.
- Enter a proposed change and its new value.
- Save a scenario separately from the original process.
- View saved scenarios.

### 4. Dependency and Impact Analysis
- Represent activities and dependencies as a directed graph.
- Identify directly connected activities.
- Find downstream activities.
- Separate direct and indirect impacts.
- Identify affected approvals and outputs.
- Display affected activities in a readable result.

### 5. Process Simulation
- Simulate the original process.
- Simulate a modified scenario.
- Compare original and modified execution paths.
- Identify activities skipped after a change.
- Compare the final outputs of both simulations.

### 6. Browser Interface
- View the application dashboard.
- Create and view processes.
- Open process details.
- Add activities and dependencies.
- View impact analysis results.
- Create and view change scenarios.
- Compare original and modified simulations.

## Functional Requirements

The project contains 50 functional requirements in the following areas:

| Group | Requirement IDs | Area |
|---|---|---|
| A | FR-01 to FR-12 | Process Analyst Requirements |
| B | FR-13 to FR-18 | Process Import and Validation Requirements |
| C | FR-19 to FR-25 | Change Scenario Requirements |
| D | FR-26 to FR-32 | Dependency Analysis Requirements |
| E | FR-33 to FR-40 | Process Simulation Requirements |
| F | FR-41 to FR-46 | Visualization and Reporting Requirements |
| G | FR-47 to FR-50 | System Administration Requirements |

Some requirements are implemented and tested, while others are still planned. The project will be updated as the remaining features are developed and tested.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Main programming language |
| Flask | Web application framework and API routes |
| SQLite | Local relational database |
| Python `sqlite3` | Database access |
| NetworkX | Directed graphs, cycle detection, and impact analysis |
| HTML | Browser page structure |
| CSS | Browser page styling |
| JSON | Process import/export and API data |
| pytest | Automated testing |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and source-code hosting |

The application uses Python's built-in `sqlite3` module. A separate SQLite package or Flask-SQLAlchemy is not required.

## Project Structure

```text
process_change_impact_simulator/
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
├── examples/
│   ├── sample_process.json
│   └── invalid_process.json
│
├── src/
│   └── process_simulator/
│       ├── __init__.py
│       ├── database.py
│       ├── schema.sql
│       ├── repository.py
│       ├── graph.py
│       ├── importer.py
│       ├── routes.py
│       ├── validators.py
│       ├── process_service.py
│       ├── dependency_service.py
│       ├── impact_service.py
│       │
│       ├── templates/
│       │   ├── base.html
│       │   ├── dashboard.html
│       │   ├── process_list.html
│       │   ├── process_detail.html
│       │   ├── impact_results.html
│       │   └── error.html
│       │
│       └── static/
│           └── css/
│               └── style.css
│
└── tests/
    ├── conftest.py
    ├── test_core.py
    ├── test_process_integration.py
    ├── test_dependency_integration.py
    ├── test_impact_integration.py
    └── test_week3_extended.py
```

### Main File Responsibilities

| File or folder | Responsibility |
|---|---|
| `app.py` | Starts the Flask application. |
| `config.py` | Stores application and database configuration. |
| `requirements.txt` | Lists the Python packages required by the project. |
| `database.py` | Creates database connections and initializes the database. |
| `schema.sql` | Defines the SQLite database tables. |
| `repository.py` | Handles database operations for stored project data. |
| `graph.py` | Builds the directed graph and supports dependency analysis. |
| `importer.py` | Handles JSON process import and related validation. |
| `routes.py` | Defines the Flask routes and API endpoints. |
| `validators.py` | Checks process and activity information. |
| `process_service.py` | Handles process-related operations. |
| `dependency_service.py` | Handles activity dependencies. |
| `impact_service.py` | Calculates the activities affected by a change. |
| `templates/` | Contains the HTML pages displayed in the browser. |
| `static/css/style.css` | Contains the browser interface styles. |
| `examples/` | Contains sample JSON process files. |
| `tests/` | Contains automated tests. |
| `instance/` | Stores the local SQLite database created by the application. |

The database file is created when the application initializes. It should not be committed to GitHub.

## Requirements

- Windows 10 or later, macOS, or Linux.
- Python 3.13 (the development environment used for this project).
- Visual Studio Code or another Python editor.
- A modern web browser.
- Internet access for installing the Python packages.

Check the Python version:

```powershell
python --version
```

## Installation and Setup

### Windows PowerShell

1. Clone the repository or download the project files.
2. Open the project folder in Visual Studio Code.
3. Open a PowerShell terminal in the project root.
4. Create a virtual environment:

```powershell
py -3.13 -m venv .venv
```

5. Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run this command in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

6. Upgrade pip and install the required packages:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

7. Set the source folder path:

```powershell
$env:PYTHONPATH = "src"
```

8. Start the application:

```powershell
python app.py
```

9. Open this address in your browser:

```text
http://127.0.0.1:5000
```

The Flask application should open and display the Process Change Impact Simulator dashboard.

### macOS or Linux

From the project root, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
export PYTHONPATH=src
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Running the Application

Each time you want to run the project on Windows:

1. Open PowerShell in the project folder.
2. Activate the virtual environment.
3. Set `PYTHONPATH`.
4. Start the Flask application.

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python app.py
```

Keep the terminal open while using the application. To stop the server, press `Ctrl + C`.

## Using the Application

The following sample workflow can be used to check the main features:

1. Open the dashboard in the browser.
2. Create a process named `Purchase Approval Workflow`.
3. Add these activities:
   - `Submit Purchase Request` – Task
   - `Manager Approval` – Approval
   - `Create Purchase Order` – Output
4. Add dependencies in this order:
   - Submit Purchase Request → Manager Approval
   - Manager Approval → Create Purchase Order
5. Open the impact analysis for `Submit Purchase Request`.
6. Check the direct and indirect affected activities.
7. Create a change scenario named `Skip Manager Approval`.
8. Select `Manager Approval` as the target activity.
9. Select the `Skip activity` change and set its value to `true`.
10. Run the simulation comparison.
11. Review the original and modified results.

In this example, the original process runs all three activities. The modified simulation skips Manager Approval and Create Purchase Order.

## JSON Examples

Sample process files are available in the `examples/` folder:

- `sample_process.json` contains a sample process definition.
- `invalid_process.json` contains invalid process data for validation testing.

The application supports JSON process import and export through its available routes. Use the sample files when testing these operations.

## Database

The application uses SQLite to store process information.

The database is created automatically when the application starts. The database schema is located at:

```text
src/process_simulator/schema.sql
```

The local database is stored under the `instance/` folder.

The main database records include:

- Processes
- Activities
- Dependencies
- Change scenarios

Do not delete the database file if you need to keep the saved project data. Local database files are excluded from GitHub.

## Testing

Run the automated tests from the project root. Make sure the virtual environment is active and `PYTHONPATH` is set.

```powershell
$env:PYTHONPATH = "src"
python -m pytest -v
```

To display a shorter test summary:

```powershell
python -m pytest -q
```

The latest test run completed successfully:

```text
11 passed
```

The tests cover the main process operations, dependency handling, impact analysis, validation, and integrated application workflows.

If a test fails, read the error message in the terminal and check the relevant route, service, template, or test before making changes.

## Current Project Status

The application currently supports:

- Creating and viewing processes.
- Adding activities to a process.
- Adding dependencies between activities.
- Storing process information in SQLite.
- Importing and exporting process information using JSON.
- Validating process information and dependency references.
- Detecting circular dependencies.
- Identifying direct and indirect downstream impacts.
- Creating and viewing change scenarios.
- Running a basic skip-activity simulation.
- Comparing original and modified simulation results.
- Using the main browser pages for the process workflow.

The following features still need more development:

- Complete editing and deletion controls for processes, activities, and dependencies.
- Full support for editing and deleting saved scenarios.
- More advanced decision and process-condition handling.
- A visual dependency graph with affected activities highlighted.
- Exporting impact analysis results as a report.
- Manager and administrator access controls.
- An administrator page for reviewing application errors and cleaning up test data.
- More testing for additional process and scenario types.

## Further Project Development Plan

The next development tasks are:

1. I plan to add options to edit and delete processes and activities.
2. The next task is to add options for editing and removing dependencies.
3. I would like to create a visual graph to show process activities and their connections.
4. I also plan to improve the simulation to support decision conditions and more process changes.
5. Finally, I intend to add report export and administrator features and test all the new functions.

After these tasks, I will review the functional requirements, fix any remaining issues, improve the user interface, and prepare the final project demonstration and documentation.

## Git and GitHub

Check which files have changed:

```powershell
git status
```

Add the project files:

```powershell
git add .
```

Commit the changes:

```powershell
git commit -m "Update Process Change Impact Simulator"
```

Push the changes to GitHub:

```powershell
git push
```

If the GitHub remote has not been configured yet, add your repository URL:

```powershell
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git branch -M main
git push -u origin main
```

Repository: https://github.com/jampally-oss/FA26_Ampally_Jagruthi_COMP_699_A

Before pushing, check that `.venv/`, local database files, cache folders, and secret configuration files are not included in the commit.

## .gitignore

The `.gitignore` file should exclude local and temporary files:

```gitignore
# Python cache
__pycache__/
*.py[cod]
.pytest_cache/

# Virtual environments
.venv/
venv/

# Local environment and secrets
.env
.env.*
!.env.example

# SQLite database files
instance/*.db
*.sqlite
*.sqlite3

# Editor and operating system files
.vscode/
.DS_Store
Thumbs.db
```

## Project Purpose

This project demonstrates how a proposed change in one part of a business process can affect connected activities and final outputs. It provides a working foundation for process management, dependency analysis, and basic change simulation, with further development planned for visualization, reporting, and administration.
