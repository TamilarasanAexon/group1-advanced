import json
import threading
from urllib.request import ProxyHandler, build_opener

from app.main import Handler
from http.server import HTTPServer


def start_test_server():
    """Start the API server on an available local port."""
    server = HTTPServer(("127.0.0.1", 0), Handler)

    thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    port = server.server_address[1]

    return server, thread, port


def test_health_endpoint():
    """Verify that the health endpoint returns HTTP 200 and status ok."""
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))

        response = opener.open(
            f"http://127.0.0.1:{port}/health"
        )

        assert response.status == 200

        body = json.loads(
            response.read().decode("utf-8")
        )

        assert body["status"] == "ok"

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_doc_endpoint():
    """Verify that the Swagger documentation page is available."""
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))

        response = opener.open(
            f"http://127.0.0.1:{port}/doc"
        )

        assert response.status == 200

        content_type = response.headers.get(
            "Content-Type",
            "",
        ).lower()

        body = response.read().decode("utf-8")

        assert "text/html" in content_type
        assert "swagger" in body.lower()
        assert "Acme Retail Inventory Management System" in body

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)