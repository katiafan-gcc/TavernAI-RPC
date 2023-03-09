import http.server
import socketserver
from http import HTTPStatus
import pypresence
import json
import time

client_id = "1078188469458841690"  # replace with your Discord application's client ID
rpc = pypresence.Presence(client_id)
rpc.connect()

PORT = 8000

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        ch_name = data.get('ch_name','')
        avatar_str = "C:/Users/Maks/Downloads/newtavern/Tavern/TavernAI/public/characters/" + ch_name + ".png"
        print(avatar_str)
        rpc.update(details=ch_name, large_image=avatar_str)
        self.send_response(HTTPStatus.OK)
        self.end_headers()

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()