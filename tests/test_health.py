def test_health_endpoint(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.is_json
    data = rv.get_json()
    assert data.get("status") == "ok"
