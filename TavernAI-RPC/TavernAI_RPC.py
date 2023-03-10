import http.server
import socketserver
from http import HTTPStatus
import pypresence
import json
import os
import requests

client_id = "1078188469458841690"
rpc = pypresence.Presence(client_id)
rpc.connect()

url = "https://catbox.moe/user/api.php"
characters = {}
file = "userinfo.txt"

# good morning sirs
def checkCharExists(name):
    with open(file, 'r') as f:
        for line in f:
            chardata = line.split("|")
            if name in chardata[0]:
                temp = chardata[1]
                cleaned = temp.strip("\n")
                chardata[1] = cleaned
                return chardata
            else:
                continue

    return False

if not os.path.exists(file):
    with open(file, "w") as f:
        PORT = input("Please enter the port that TavernAI is running on (leave blank if default): ")
        if PORT:
            f.write(PORT)
        else:
            f.write("8000")

with open(file, "r") as f:
    PORT = f.readline()

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # getting the character name
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        ch_name = data.get('ch_name', '')
        chardata = checkCharExists(ch_name)

        # check if character exists already
        if chardata:
            rpc.update(details="Talking to: " + chardata[0],
                       large_image=chardata[1],
                       large_text="Currently Roleplaying",
                       small_image="tavern")

        # otherwise do stuff
        else:
            avatar_path = os.path.abspath("C:/Users/thatr/Documents/newtavern/Tavern/TavernAI/public/characters/" + ch_name + ".png")
            avatar_url = "file:///" + avatar_path.replace("\\", "/")

            # send request to catbox.moe
            with open(avatar_path, "rb") as f:
                files = {"fileToUpload": f}
                data = {"reqtype": "fileupload", "userhash": ""}
                response = requests.post(url, data=data, files=files)

            rpc.update(details="Talking to: " + ch_name, 
                       large_image=response.text, 
                       large_text="Currently Roleplaying",
                       small_image="tavern")
            
            # save new character
            characters[ch_name] = response.text
            with open(file, 'a') as f:
                f.write("\n" + ch_name + "|" + characters.get(ch_name))

        self.send_response(HTTPStatus.OK)
        self.end_headers()

with socketserver.TCPServer(("", int(PORT)), MyRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()