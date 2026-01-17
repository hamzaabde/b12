import http.server
import socketserver


PORT = 8000

class EchoHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        response = f'GET request received. Path: {self.path}\nHeaders:\n{self.headers}'
        self.wfile.write(bytes(response, "utf-8"))
        print(response)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        print(self.headers)
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = f'POST request received. Path: {self.path}\nHeaders:\n{self.headers}\nBody:\n{post_data.decode("utf-8")}'
        self.wfile.write(bytes(response, "utf-8"))
        print(response)

    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(("", PORT), EchoHandler) as httpd:
    print(f"Serving HTTP echo on port {PORT}")
    httpd.serve_forever()
