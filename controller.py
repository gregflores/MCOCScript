import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyController

class Controller:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyController()

    def click_on_window(self):
        self.mouse.position = (100, 350)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        self.mouse.position = (2000, 350)
    
    def click_button(self, x, y):
        self.mouse.position = (x, y)
        self.mouse.press(Button.left)
        self.mouse.release(Button.left)
        self.mouse.position = (2000, 350)

    def action_key(self, action, interval=0.1):
        self.keyboard.press(action)
        time.sleep(interval)
        self.keyboard.release(action)
        #print(action)

