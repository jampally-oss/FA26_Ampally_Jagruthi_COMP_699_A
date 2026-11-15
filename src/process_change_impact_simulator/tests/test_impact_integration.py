def test_end_to_end_impact_result_contains_direct_indirect_and_path(client):
    process = client.post("/api/processes", json={"name": "Purchase Approval"}).get_json()
    pid = process["id"]
    activity_ids = []
    for name, kind in [("Submit Request", "task"), ("Manager Approval", "approval"), ("Create Purchase Order", "output")]:
        activity = client.post(f"/api/processes/{pid}/activities", json={"name": name, "activity_type": kind}).get_json()
        activity_ids.append(activity["id"])
    for source, target in zip(activity_ids, activity_ids[1:]):
        assert client.post(f"/api/processes/{pid}/dependencies", json={"predecessor_id": source, "successor_id": target}).status_code == 201
    result = client.get(f"/api/processes/{pid}/activities/{activity_ids[0]}/impact")
    assert result.status_code == 200
    data = result.get_json()
    assert [x["name"] for x in data["direct_downstream"]] == ["Manager Approval"]
    assert [x["name"] for x in data["indirect_downstream"]] == ["Create Purchase Order"]
    assert data["affected_special_types"][0]["activity_type"] == "approval"
    assert data["paths"][0][0]["name"] == "Submit Request"
