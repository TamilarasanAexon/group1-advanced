import json
from http.server import HTTPServer
from threading import Thread
from urllib.request import build_opener, ProxyHandler

from app.main import Handler


def start_test_server():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]

    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    return server, thread, port


def test_health_endpoint():
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))
        response = opener.open(
            f"http://127.0.0.1:{port}/health"
        )

        assert response.status == 200

        body = json.loads(response.read().decode())
        assert body == {"status": "ok"}

    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_doc_endpoint():
    server, thread, port = start_test_server()

    try:
        opener = build_opener(ProxyHandler({}))
        response = opener.open(
            f"http://127.0.0.1:{port}/doc"
        )

        assert response.status == 200

        body = json.loads(response.read().decode())

        assert body["service"] == "inventory-management-system"
        assert body["version"] == "1.0.0"

        paths = [
            endpoint["path"]
            for endpoint in body["endpoints"]
        ]

        assert "/" in paths
        assert "/health" in paths
        assert "/doc" in paths

    finally:
        server.shutdown()
        server.server_close()
        thread.join()