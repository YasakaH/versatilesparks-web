"""Local web server to view an agent run timeline.

Usage:
    python -m agent_replay.viewer.serve <run_id>
"""

import json
import os
import sys
import http.server
import socketserver
import webbrowser
import threading

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_replay import run_to_json


TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "index.html")


def serve_run(run, port=3456):
    """Serve a single run as a local web page."""
    run_json = run_to_json(run)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                if os.path.exists(TEMPLATE_PATH):
                    with open(TEMPLATE_PATH, "r") as f:
                        html = f.read()
                    # Inject run data
                    html = html.replace("/* RUN_DATA_PLACEHOLDER */", 
                        f"const RUN_DATA = {run_json};")
                    self.wfile.write(html.encode())
                else:
                    self.wfile.write(b"<h1>Template not found</h1>")
            elif self.path == "/data":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(run_json.encode())
            else:
                self.send_response(404)
                self.end_headers()

    server = socketserver.TCPServer(("", port), Handler)
    url = f"http://localhost:{port}"

    print(f"Agent Replay Viewer — {run.agent.name}")
    print(f"Run: {run.run_id} | Events: {len(run.events)} | Status: {run.status}")
    print(f"Goal: {run.goal}")
    print(f"\nOpen: {url}")
    print("Press Ctrl+C to stop.\n")

    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python serve.py <run_id>")
        sys.exit(1)
    from agent_replay import load, load_path
    run = load(sys.argv[1]) or load_path(sys.argv[1])
    if run is None:
        print(f"Run '{sys.argv[1]}' not found.")
        sys.exit(1)
    serve_run(run)
