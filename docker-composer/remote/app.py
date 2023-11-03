from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs

hostName = "0.0.0.0"
script_dir = os.path.dirname(os.path.realpath(__file__))

def read_file(file):
    try:
        file_path = os.path.join(script_dir, 'files', file + '.txt')
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return None
    except Exception as e:
        return None
class MyHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, content_type, response_body):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(response_body.encode('utf-8'))

    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if 'q' not in query_params:
            self._send_response(400, 'text/plain', 'Missing "q" query parameter')
            return
            
        param_value = query_params['q'][0]
        file_content = read_file(param_value)
        if file_content is None:
            self._send_response(404, 'text/plain', 'File not found')
            return
        
        response_data = {'file_content': file_content}
        response_body = json.dumps(response_data)
        self._send_response(200, 'application/json', response_body)

def run(port=8080):
    server_address = (hostName, port)
    print("Server started http://%s:%s" % server_address)
    webServer = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...')
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    run()
