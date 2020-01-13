import cv2
import numpy as np

from vision import Vision
from controller import Controller
from game import Game


#img = cv2.imread(r'C:\Users\flore\Documents\Python Scripts\MCOCScript\images\help-button.png', 0)
#cv2.imshow('window', img)
#lol
#LMAO
vision = Vision()
controller = Controller()
game = Game(vision, controller)

# screenshot = vision.get_image('tests/screens/round-finished-results.png')
# print(screenshot)
# match = vision.find_template('bison-head', image=screenshot)
# print(np.shape(match)[1])

game.run()
