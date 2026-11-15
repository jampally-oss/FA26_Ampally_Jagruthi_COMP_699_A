def test_browser_workflow_creates_and_retrieves_process(client):
    response = client.post("/processes", data={"name": "Purchase Approval", "description": "Purchase request workflow"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Purchase Approval" in response.data
    listing = client.get("/processes")
    assert b"Purchase Approval" in listing.data
    
