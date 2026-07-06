import pytest

SECTION_ENDPOINTS = [
    ("/experience/", {"company": "Corp", "role": "Dev", "description": "Worked", "start_date": "2024", "order": 1}),
    ("/education/", {"institution": "U", "degree": "BSc", "description": "Studied", "year": "2024"}),
    ("/skills/", {"name": "Python", "level": 90, "category": "Backend", "order": 1}),
    ("/projects/", {"title": "Proj", "description": "Desc", "image_url": "", "repo_url": "", "demo_url": "", "featured": False, "order": 1}),
    ("/courses/", {"title": "Course", "platform": "Udemy", "certificate_url": "", "date": "2024"}),
    ("/blog/", {"title": "Post", "slug": "test-post", "content_md": "# Hello"}),
]


class TestSectionCRUD:
    @pytest.mark.parametrize("endpoint,payload", SECTION_ENDPOINTS)
    def test_get_empty(self, client, endpoint, payload):
        r = client.get(endpoint)
        assert r.status_code == 200
        assert r.json() == []

    @pytest.mark.parametrize("endpoint,payload", SECTION_ENDPOINTS)
    def test_create_unauthorized(self, client, endpoint, payload):
        r = client.post(endpoint, json=payload)
        assert r.status_code in (403, 401)

    @pytest.mark.parametrize("endpoint,payload", SECTION_ENDPOINTS)
    def test_create_and_get(self, client, auth_headers, endpoint, payload):
        r = client.post(endpoint, json=payload, headers=auth_headers)
        assert r.status_code == 200, f"POST {endpoint} failed: {r.text}"
        created = r.json()
        assert created["id"] >= 1

        r = client.get(endpoint)
        assert r.status_code == 200
        items = r.json()
        assert len(items) == 1
        assert items[0]["id"] == created["id"]

    @pytest.mark.parametrize("endpoint,payload", [
        ("/experience/", {"company": "New Corp"}),
        ("/education/", {"institution": "New U"}),
        ("/skills/", {"name": "New Skill"}),
        ("/projects/", {"title": "New Proj"}),
        ("/courses/", {"title": "New Course"}),
        ("/blog/", {"title": "New Post"}),
    ])
    def test_update(self, client, auth_headers, endpoint, payload):
        create = client.post(endpoint, json=self._create_payload(endpoint), headers=auth_headers)
        item_id = create.json()["id"]
        r = client.put(f"{endpoint}{item_id}", json=payload, headers=auth_headers)
        assert r.status_code == 200, f"PUT {endpoint}{item_id} failed: {r.text}"

    def _create_payload(self, endpoint):
        for ep, pl in SECTION_ENDPOINTS:
            if ep == endpoint:
                return pl
        return {}

    @pytest.mark.parametrize("endpoint,payload", SECTION_ENDPOINTS)
    def test_delete(self, client, auth_headers, endpoint, payload):
        create = client.post(endpoint, json=payload, headers=auth_headers)
        item_id = create.json()["id"]
        r = client.delete(f"{endpoint}{item_id}", headers=auth_headers)
        assert r.status_code == 200
        r = client.get(endpoint)
        assert r.json() == []
