import http.server
import socketserver
from http import HTTPStatus
import pypresence
import json
import os
import requests

client_id = "1078188469458841690"  # replace with your Discord application's client ID
rpc = pypresence.Presence(client_id)
rpc.connect()

url = "https://catbox.moe/user/api.php"

PORT = 8000

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        ch_name = data.get('ch_name', '')
        avatar_path = os.path.abspath("C:/Users/thatr/Documents/newtavern/Tavern/TavernAI/public/characters/" + ch_name + ".png")
        avatar_url = "file:///" + avatar_path.replace("\\", "/")

        with open(avatar_path, "rb") as f:
            files = {"fileToUpload": f}
            data = {"reqtype": "fileupload", "userhash": ""}
            response = requests.post(url, data=data, files=files)

        rpc.update(details="Talking to: " + ch_name, 
                   large_image=response.text, 
                   large_text="Probably fucking her"
                   )
        self.send_response(HTTPStatus.OK)
        self.end_headers()

with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()