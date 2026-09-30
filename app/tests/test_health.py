import json
import threading
from urllib.request import ProxyHandler, build_opener

# Adjust this import only if your main.py exposes a different server factory/class.
from app.main import create_server


def start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    port = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    return server, thread, port


def test_health_endpoint():
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))
        response = opener.open(f"http://127.0.0.1:{port}/health")

        assert response.status == 200

        body = json.loads(response.read().decode("utf-8"))
        assert body["status"] == "ok"

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_doc_endpoint():
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))
        response = opener.open(f"http://127.0.0.1:{port}/doc")

        assert response.status == 200

        content_type = response.headers.get("Content-Type", "").lower()
        body = response.read().decode("utf-8")

        # /doc is now the interactive Swagger documentation page.
        # Do not parse it as the old JSON documentation response.
        assert "text/html" in content_type
        assert "swagger" in body.lower()
        assert "Acme Retail Inventory Management System" in body

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
