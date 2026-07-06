def test_get_public_profile(client):
    r = client.get("/profile/")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Giovapolis"
    assert body["title"] == "Dev"
    assert body["email"] == "giovapolis@portfolio.com"


def test_update_profile_unauthorized(client):
    r = client.put("/profile/", json={"name": "Hacker"})
    assert r.status_code == 401


def test_update_profile_success(client, auth_headers):
    r = client.put("/profile/", json={"title": "Senior Dev", "location": "Mexico City"}, headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == "Senior Dev"
    assert body["location"] == "Mexico City"


def test_update_profile_partial(client, auth_headers):
    r = client.put("/profile/", json={"bio": "Updated bio"}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["bio"] == "Updated bio"
