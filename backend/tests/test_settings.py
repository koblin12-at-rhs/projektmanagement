def login(client, username="admin", password="secret"):
    return client.post("/api/auth/local/login", json={"username": username, "password": password})


def test_project_requests_can_be_disabled(client):
    login(client)
    client.put("/api/admin/settings/projects.allow_new_requests", json={"value": "false"})
    response = client.post("/api/projects", json={"title": "Roboterarm"})
    assert response.status_code == 403
    assert "Projektanfragen" in response.get_json()["message"]


def test_dynamic_texts_are_loaded(client):
    login(client)
    response = client.get("/api/admin/texts")
    assert response.status_code == 200
    keys = {item["key"] for item in response.get_json()}
    assert "button.new_project" in keys


def test_settings_require_admin_permission(client):
    login(client, username="user", password="secret")
    response = client.get("/api/admin/settings")
    assert response.status_code == 403
