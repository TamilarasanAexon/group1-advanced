from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = int(os.getenv("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):

    def _send(self, status, payload):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/":
            self._send(
                200,
                {
                    "service": "inventory-management-system",
                    "version": "1.0.0"
                }
            )

        elif self.path == "/health":
            self._send(
                200,
                {
                    "status": "ok"
                }
            )

        elif self.path == "/doc":
            self._send(
                200,
                {
                    "service": "inventory-management-system",
                    "version": "1.0.0",
                    "endpoints": [
                        {
                            "method": "GET",
                            "path": "/",
                            "description": "Service information"
                        },
                        {
                            "method": "GET",
                            "path": "/health",
                            "description": "Service health check"
                        },
                        {
                            "method": "GET",
                            "path": "/doc",
                            "description": "API documentation"
                        }
                    ]
                }
            )

        else:
            self._send(
                404,
                {
                    "error": "not found"
                }
            )


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), Handler)

    print(f"API running on http://127.0.0.1:{PORT}")

    server.serve_forever()