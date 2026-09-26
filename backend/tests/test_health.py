from fastapi.testclient import TestClient

from ptrack.config import Settings, get_settings
from ptrack.main import app


def test_health_reports_ok_with_no_carriers():
    app.dependency_overrides[get_settings] = lambda: Settings(_env_file=None)
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["carriers_configured"] == []
    app.dependency_overrides.clear()


def test_health_lists_configured_carriers_without_leaking_keys():
    settings = Settings(_env_file=None, dhl_api_key="secret-value", fedex_api_key="k")
    app.dependency_overrides[get_settings] = lambda: settings
    client = TestClient(app)

    body = client.get("/health").json()

    assert body["carriers_configured"] == ["dhl"]
    assert "secret-value" not in str(body)
    app.dependency_overrides.clear()
