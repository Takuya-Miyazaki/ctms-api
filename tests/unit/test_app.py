"""pytest tests for basic app functionality"""


def test_read_root(client):
    """The site root redirects to the Swagger docs"""
    resp = client.get("/")
    assert resp.status_code == 200
    assert len(resp.history) == 1
    prev_resp = resp.history[0]
    assert prev_resp.status_code == 307  # Temporary Redirect
    assert prev_resp.headers["location"] == "./docs"


def test_read_health(client):
    """The platform calls /health to check app readiness."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == [{"health": "OK"}, 200]
