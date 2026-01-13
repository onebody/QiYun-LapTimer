import http.server
import socketserver
import json
import os

PORT = 8002

class MockESP32Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/nodes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Use localhost:8002 for the mock node so it connects back to this server
            response = {"nodes": [{"product": "MockESP32", "host": "esp32-mock", "ip": "localhost:8002", "mac": "00:00:00:00:00:00"}]}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/events':
            # Mock SSE connection (just keep it open or close it immediately)
            # SimpleHTTPRequestHandler doesn't support keeping connection open easily without blocking
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(b"data: connected\n\n")
        else:
            super().do_GET()

    def do_POST(self):
        # Handle POST requests by returning success
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        print(f"POST request to {self.path} with body: {post_data.decode('utf-8')}")

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'{"status": "ok", "message": "Mock response"}')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

with socketserver.TCPServer(("", PORT), MockESP32Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
