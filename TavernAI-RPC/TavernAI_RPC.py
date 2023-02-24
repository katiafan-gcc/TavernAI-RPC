import pyautogui
import time
from selenium import webdriver
from pypresence import Presence

# Initialize the Discord Rich Presence client
client_id = '1078188469458841690'
RPC = Presence(client_id)
RPC.connect()

RPC.update(state='Browsing the web', details='Chrome', large_image='chrome')

# Initialize the Selenium WebDriver for Chrome
driver = webdriver.Chrome()

while True:
    # Get the title of the current Chrome tab
    current_tab_title = pyautogui.getActiveWindowTitle()
    print(pyautogui.getActiveWindowTitle())

    if current_tab_title == 'Tavern.AI - Google Chrome':
        # Load the TavernAI website
        driver.get('http://127.0.0.1:8000')

        # Wait for the page to load
        time.sleep(5)

        # Get the name of the current channel on TavernAI
        channel_name_element = driver.find_element_by_class_name('ch_name')
        channel_name = channel_name_element.get_attribute('innerHTML').strip()

        # Set the presence if the user is on the TavernAI tab
        RPC.update(state='Playing TavernAI', details=f'In #{channel_name}', large_image='tavernai', small_image='playing')

    time.sleep(5)

# Close the Selenium WebDriver and RPC connection when done
driver.quit()
RPC.close()