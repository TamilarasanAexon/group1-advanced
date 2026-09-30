from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """Verify the health endpoint."""

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }


def test_root_endpoint():
    """Verify the root endpoint."""

    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["service"] == "inventory-management-system"
    assert body["version"] == "1.0.0"
    assert body["status"] == "running"


def test_swagger_doc_endpoint():
    """Verify Swagger UI is available."""

    response = client.get("/doc")

    assert response.status_code == 200

    content_type = response.headers.get(
        "content-type",
        ""
    ).lower()

    assert "text/html" in content_type
    assert "swagger" in response.text.lower()


def test_openapi_endpoint():
    """Verify the OpenAPI schema."""

    response = client.get("/openapi.json")

    assert response.status_code == 200

    body = response.json()

    assert (
        body["info"]["title"]
        == "Acme Retail Inventory Management System"
    )

    assert body["info"]["version"] == "1.0.0"

    assert "/health" in body["paths"]
    assert "/products" in body["paths"]


def test_products_endpoint():
    """Verify products endpoint."""

    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)