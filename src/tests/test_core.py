def test_create_list_add_activity_and_dependency(client):
    p=client.post("/api/processes",json={"name":"Onboarding"}); assert p.status_code==201
    pid=p.get_json()["id"]; assert len(client.get("/api/processes").get_json())==1
    a=client.post(f"/api/processes/{pid}/activities",json={"name":"Submit","activity_type":"task"}).get_json()
    b=client.post(f"/api/processes/{pid}/activities",json={"name":"Approve","activity_type":"approval"}).get_json()
    assert client.post(f"/api/processes/{pid}/dependencies",json={"predecessor_id":a["id"],"successor_id":b["id"]}).status_code==201
def test_downstream_impact(client):
    p=client.post("/api/processes",json={"name":"Flow"}).get_json(); pid=p["id"]
    ids=[]
    for name in ["Start","Review","Output"]:
        ids.append(client.post(f"/api/processes/{pid}/activities",json={"name":name}).get_json()["id"])
    for a,b in zip(ids,ids[1:]):
        assert client.post(f"/api/processes/{pid}/dependencies",json={"predecessor_id":a,"successor_id":b}).status_code==201
    result=client.get(f"/api/processes/{pid}/activities/{ids[0]}/impact").get_json()
    assert [x["id"] for x in result["direct_downstream"]]==[ids[1]]
    assert [x["id"] for x in result["indirect_downstream"]]==[ids[2]]
def test_import_and_validation(client):
    doc={"process":{"name":"Imported"},"activities":[{"key":"a","name":"Start"},{"key":"b","name":"Finish"}],"dependencies":[{"from":"a","to":"b"}]}
    assert client.post("/api/import",json=doc).status_code==201
    doc["dependencies"]=[{"from":"a","to":"missing"}]
    response=client.post("/api/import",json=doc)
    assert response.status_code==400
def test_import_rejects_cycle(client):
    doc={"process":{"name":"Cycle"},"activities":[{"key":"a","name":"A"},{"key":"b","name":"B"}],"dependencies":[{"from":"a","to":"b"},{"from":"b","to":"a"}]}
    assert client.post("/api/import",json=doc).status_code==400
