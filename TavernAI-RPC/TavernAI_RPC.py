import win32com.client
import requests
from bs4 import BeautifulSoup
from pypresence import Presence
import time

# Initialize the Discord Rich Presence client
client_id = '1078188469458841690'
RPC = Presence(client_id)
RPC.connect()

# Create a web server that serves the HTML page containing the title tag
# using Flask, for example:
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)

# Connect to the running Chrome browser
chrome = win32com.client.Dispatch("ChromeTab.ChromeTabWrapper")

while True:
    # Retrieve the HTML page containing the title tag
    response = requests.get('http://127.0.0.1:8000')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title tag from the HTML
    title = soup.find('title').text

    # Update the Discord Rich Presence status with the title of the web page
    RPC.update(details=title)

    # Sleep for 15 seconds before checking for a new title
    time.sleep(15)