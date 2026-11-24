from process_simulator import repository as repo
from process_simulator.validators import validate_process_payload, validate_activity_payload

class ValidationError(ValueError):
    pass

def create_process(path, payload):
    errors = validate_process_payload(payload)
    if errors:
        raise ValidationError(" ".join(errors))
    pid = repo.create_process(path, payload["name"].strip(), payload.get("description", "").strip())
    return repo.process(path, pid)

def add_activity(path, pid, payload):
    if not repo.process(path, pid):
        raise LookupError("Process not found.")
    errors = validate_activity_payload(payload)
    if errors:
        raise ValidationError(" ".join(errors))
    aid = repo.add_activity(path, pid, payload["name"].strip(),
        payload.get("description", "").strip(), payload.get("activity_type", "task"),
        payload.get("condition_expression", "").strip())
    return next(a for a in repo.activities(path, pid) if a["id"] == aid)
