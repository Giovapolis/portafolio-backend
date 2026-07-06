def test_login_success(client):
    r = client.post("/auth/login", data={"username": "Giovapolis", "password": "GioAdmin2026"})
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    assert body["user"]["username"] == "Giovapolis"


def test_login_invalid_password(client):
    r = client.post("/auth/login", data={"username": "Giovapolis", "password": "wrong"})
    assert r.status_code == 401


def test_login_invalid_user(client):
    r = client.post("/auth/login", data={"username": "unknown", "password": "x"})
    assert r.status_code == 401


def test_me_success(client, auth_headers):
    r = client.get("/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["username"] == "Giovapolis"


def test_me_unauthorized(client):
    r = client.get("/auth/me")
    assert r.status_code == 401
