def test_dependency_saved_and_cycle_rejected(client):
    p = client.post("/api/processes", json={"name": "Purchase Flow"}).get_json()
    pid = p["id"]
    ids = [client.post(f"/api/processes/{pid}/activities", json={"name": n}).get_json()["id"] for n in ["Submit", "Approve", "Order"]]
    assert client.post(f"/api/processes/{pid}/dependencies", json={"predecessor_id": ids[0], "successor_id": ids[1]}).status_code == 201
    assert client.post(f"/api/processes/{pid}/dependencies", json={"predecessor_id": ids[1], "successor_id": ids[2]}).status_code == 201
    cycle = client.post(f"/api/processes/{pid}/dependencies", json={"predecessor_id": ids[2], "successor_id": ids[0]})
    assert cycle.status_code == 409
    saved = client.get(f"/api/processes/{pid}").get_json()
    assert len(saved["dependencies"]) == 2
