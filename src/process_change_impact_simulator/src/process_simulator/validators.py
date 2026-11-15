ACTIVITY_TYPES = {"task", "decision", "approval", "output"}

def validate_process_payload(data):
    errors = []
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("Process name is required.")
    description = data.get("description", "")
    if not isinstance(description, str):
        errors.append("Process description must be text.")
    return errors

def validate_activity_payload(data):
    errors = []
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("Activity name is required.")
    if data.get("activity_type", "task") not in ACTIVITY_TYPES:
        errors.append("Activity type must be task, decision, approval, or output.")
    if not isinstance(data.get("description", ""), str):
        errors.append("Activity description must be text.")
    return errors

def validate_dependency_payload(data):
    if not isinstance(data, dict):
        return ["Request body must be a JSON object."]
    try:
        a, b = int(data["predecessor_id"]), int(data["successor_id"])
    except (KeyError, TypeError, ValueError):
        return ["predecessor_id and successor_id must be integer activity IDs."]
    if a == b:
        return ["An activity cannot depend on itself."]
    return []
