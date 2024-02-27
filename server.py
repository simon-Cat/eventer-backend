from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
from _g_posts import _g_posts


class MyServer(BaseHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://127.0.0.1:5500')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        return super(MyServer, self).end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        self.wfile.write(json.dumps(_g_posts).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body.decode())

        print(type(data), data)

        response = BytesIO()
        response.write(body)

        self.wfile.write(response.getvalue())


def run(server_class=HTTPServer, handler_class=MyServer):
    print('Connection established')
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
