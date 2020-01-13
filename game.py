import numpy as np
import time
import cv2

class Game:

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'game start'



    ##States
    #Game start         - click on memu
    #Ask for help       - h
    #Load champions     - a
    #Find Match         - s
    #pick opponents     - d
    #accept config      - d
    #continue to fight  - d
    #fighting 1         - a h f g s
    #next fight         - j
    #fighting 2         - a h f g s
    #final fight        - j
    #fighting 3         - a h f g s
    #end match 3        - j
    #next series        - z

    # When the game slows down, the checks could screw up
    # Maybe check if its the first or second time we've gotten to press the button

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.state == 'game start':
                self.game_start()
            elif self.state == 'look for help':
                self.log(self.state)
                time.sleep(1)
                self.find_help()
            elif self.state == 'loading champs':
                self.log(self.state)
                time.sleep(1)
                self.load_champs()
            elif self.state == 'finding match':
                self.log(self.state)
                time.sleep(1)
                self.find_match()
            elif self.state == 'picking opponents':
                self.log(self.state)
                time.sleep(1)
                self.pick_opponents()
            elif self.state == 'accepting config':
                self.log(self.state)
                time.sleep(1)
                self.accept_config()
            elif self.state == 'continuing to fight':
                self.log(self.state)
                time.sleep(1)
                self.continue_to_fight()
            elif self.state == 'loading into fight':
                self.log(self.state)
                self.load_into_fight()
            elif self.state == 'fighting':
                self.log(self.state)
                self.fighting()
            elif self.state == 'next fight':
                self.log(self.state)
                time.sleep(1)
                self.next_fight()
            elif self.state == 'final fight':
                self.log(self.state)
                time.sleep(1)
                self.final_fight()
            elif self.state == 'ending match':
                self.log(self.state)
                time.sleep(1)
                self.end_match()
            elif self.state == 'next series':
                self.log(self.state)
                time.sleep(1)
                self.next_series()                      
            else:
                self.log('Not doing anything')
            #time.sleep(1)

    def game_start(self):
        self.controller.click_on_window()
        self.state = 'look for help'

    def find_help(self):
        matched = self.vision.find_template('help-button')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('h', 0.2)
        else :
            self.state = 'loading champs'
        

    def load_champs(self):
        matched = self.vision.find_template('empty-slot-bottom')
        time.sleep(1)
        if matched:
            self.controller.action_key('a', 0.3)
            time.sleep(1)
        else :
            self.state = 'finding match'
            
    #Create states in each method. In and Out states            
    def find_match(self):
        matched = self.vision.find_template('find-match')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('s', 0.2)
            self.state = 'picking opponents'
        else :
            self.state = 'finding match'
    
    def pick_opponents(self):
        matched = self.vision.find_template('continue')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('d', 0.2)
            self.state = 'accepting config'
        else :
            self.state = 'picking opponents'
    
    def accept_config(self):
        matched = self.vision.find_template('accept')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('d', 0.2)
            self.state = 'continuing to fight'
        else :
            self.state = 'accepting config'

    def continue_to_fight(self):
        matched = self.vision.find_template('continue')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('d', 0.2)
            self.state = 'loading into fight'
        else :
            self.state = 'continuing to fight'

    def load_into_fight(self):
        matched = self.vision.find_template('pause')
        time.sleep(0.5)
        if matched:
            self.log('found pause moving to attack')
            self.state = 'fighting'
        else:
            self.state = 'loading into fight'

    def fighting(self):
        matched = self.vision.find_template('pause')
        if matched:
            self.log('Found pause')
            self.controller.action_key('g',0.05)
            self.controller.action_key('f',0.01)
            self.controller.action_key('f',0.01)
            self.controller.action_key('f',0.01)
            self.state = 'fighting'
        else :
            self.log('ending fight')
            self.state = 'next fight'

            
    
    def next_fight(self):
        matched = self.vision.find_template('next-fight')
        matched2 = self.vision.find_template('final-fight')
        matched3 = self.vision.find_template('end-match')
        time.sleep(0.5)
        if matched:
            self.controller.action_key('j')
            self.controller.action_key('k')
            self.state = 'loading into fight'
        elif matched2:
            self.controller.action_key('j')
            self.controller.action_key('k')
            self.state = 'loading into fight'
        elif matched3:
            self.controller.action_key('j')
            self.controller.action_key('k')
            self.state = 'next series'
        else:
            self.state = 'next fight'


    def next_series(self):
        coord = self.vision.find_template_center('next-series')
        time.sleep(0.5)
        if coord:
            self.controller.click_button(coord[0], coord[1])
            time.sleep(2)
            self.state = 'look for help'
        else:
            self.state = 'next series'


    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))