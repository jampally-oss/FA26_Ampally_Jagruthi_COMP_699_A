ACTIVITY_TYPES = {"task", "decision", "approval", "output"}

def validate_process_payload(data):
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    errors = []
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        errors.append("Process name is required.")
    if not isinstance(data.get("description", ""), str):
        errors.append("Process description must be text.")
    return errors

def validate_activity_payload(data):
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    errors = []
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        errors.append("Activity name is required.")
    if data.get("activity_type", "task") not in ACTIVITY_TYPES:
        errors.append("Activity type must be task, decision, approval, or output.")
    for field in ("description", "condition_expression"):
        if not isinstance(data.get(field, ""), str):
            errors.append(f"{field} must be text.")
    return errors

def validate_dependency_payload(data):
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    try:
        a, b = int(data["predecessor_id"]), int(data["successor_id"])
    except (KeyError, TypeError, ValueError):
        return ["predecessor_id and successor_id must be integer activity IDs."]
    return ["An activity cannot depend on itself."] if a == b else []
