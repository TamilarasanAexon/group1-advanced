import json
import threading
from http.server import HTTPServer
from urllib.request import ProxyHandler, build_opener

from app.main import Handler


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
    """Verify the health endpoint."""
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
    """Verify the API documentation endpoint."""
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

        assert "application/json" in content_type

        body = json.loads(
            response.read().decode("utf-8")
        )

        assert "name" in body
        assert "version" in body
        assert "endpoints" in body

        assert body["name"] == "Group1 Advanced API"
        assert body["version"] == "1.0"

        assert "/" in body["endpoints"]
        assert "/health" in body["endpoints"]
        assert "/doc" in body["endpoints"]

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)