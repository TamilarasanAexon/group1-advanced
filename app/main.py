from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "0.0.0.0"
PORT = 8080


class Handler(BaseHTTPRequestHandler):
    def send_json_response(self, status_code, data):
        """Send a JSON response."""
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):
        if self.path == "/":
            self.send_json_response(
                200,
                {
                    "message": "Group1 Advanced API",
                    "status": "running",
                },
            )

        elif self.path == "/health":
            self.send_json_response(
                200,
                {
                    "status": "ok",
                },
            )

        elif self.path == "/doc":
            self.send_json_response(
                200,
                {
                    "name": "Group1 Advanced API",
                    "version": "1.0",
                    "endpoints": {
                        "/": "API information",
                        "/health": "Health check",
                        "/doc": "API documentation",
                    },
                },
            )

        else:
            self.send_json_response(
                404,
                {
                    "error": "Not Found",
                },
            )


def run_server():
    server = HTTPServer((HOST, PORT), Handler)

    print(
        f"API running on http://{HOST}:{PORT}",
        flush=True,
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping API...")

    finally:
        server.server_close()
        print("API stopped.")


if __name__ == "__main__":
    run_server()