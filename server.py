from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
from db import cursor


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

        cursor.execute(' SELECT * FROM events')
        all_users = cursor.fetchall()

        self.wfile.write(json.dumps(all_users).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        data = json.loads(body.decode())

        event_title = data.get('eventTitle')
        event_description = data.get('eventDescription')
        event_image = data.get('eventImage')

        # BD
        cursor.execute('INSERT INTO events (title, description, image) VALUES (%s, %s, %s)', (event_title, event_description, event_image))

        response = BytesIO()
        response.write(body)

        self.wfile.write(response.getvalue())


def run(server_class=HTTPServer, handler_class=MyServer):
    print('Connection established')
    server_address = ('localhost', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
