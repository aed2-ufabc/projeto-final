from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs
import time

hostName = "0.0.0.0"
script_dir = os.path.dirname(os.path.realpath(__file__))

def read_file(file):
    try:
        file_path = os.path.join(script_dir, 'files', file + '.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            dictionary = json.load(file)
            return dictionary
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

# Construir a árvore trie
def build_trie(dictionary):
    print("entrou aqui", flush=True)
    trie = {}
    for word, meaning in dictionary.items():
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['meaning'] = meaning
    return trie

# Função para procurar uma palavra na árvore trie
def search_word(trie, word):
    node = trie
    for char in word:
        if char in node:
            node = node[char]
        else:
            return None
    return node.get('meaning', None)

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
        
        if 'word' not in query_params:
            self._send_response(400, 'text/plain', 'Missing "word" query parameter')
            return
        
        param_value_q = query_params['q'][0]

        start_time = time.time()
        file_content = read_file(param_value_q)
        print("read_file --- %s seconds ---" % (time.time() - start_time), flush=True)

        if file_content is None:
            self._send_response(404, 'text/plain', 'File not found')
            return
        
        start_time = time.time()
        # Construir a árvore trie a partir do dicionário
        trie = build_trie(file_content)
        print("build_trie --- %s seconds ---" % (time.time() - start_time), flush=True)

        # Pedir ao usuário para inserir uma palavra
        param_value_word = query_params['word'][0]

        start_time = time.time()
        # Procurar a palavra na árvore trie
        meaning = search_word(trie, param_value_word)
        print("search_word --- %s seconds ---" % (time.time() - start_time), flush=True)

        
        response_body = meaning
        self._send_response(200, 'application/json', response_body)

def run(port=8080):
    server_address = (hostName, port)
    print("Server started http://%s:%s" % server_address, flush=True)
    webServer = HTTPServer(server_address, MyHandler)
    print(f'Starting server on port {port}...', flush=True)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.", flush=True)

if __name__ == '__main__':
    run()
