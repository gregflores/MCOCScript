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

    # DONE:When the game slows down, the checks could screw up
    # DONE:Maybe check if its the first or second time we've gotten to press the button
    #NEED TO ACCOUNT FOR MISTAKES IN LOADING AND HELPING CHAMPS


    def run(self):
        while True:
            if cv2.waitKey(1) == ord('q'):
                break
            self.vision.refresh_frame()
            if self.state == 'game start':
                self.game_start()
            elif self.state == 'champ setup':
                self.log(self.state)
                self.champ_setup()
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
        self.state = 'champ setup'


    # Check if there is an X
    # If so, press X
    # If no check for help
    # If no check for empty slot
    # If none of these are triggered, move on
    def champ_setup(self):
        matchedhelp = self.vision.find_template('help-button')
        matchedempty = self.vision.find_template('empty-slot-bottom')
        coord = self.vision.find_template_center('exit')
        time.sleep(0.5)
        if coord:
            self.controller.click_button(coord[0], coord[1])
            time.sleep(1)
        elif matchedhelp:
            self.controller.action_key('h', 0.2)
            time.sleep(1)
        elif matchedempty:
            self.controller.action_key('a', 0.3)
            time.sleep(1)
        else:
            self.state = 'finding match'
            
    #Create states in each method. In and Out states            
    def find_match(self):
        section = 'In'
        while section == 'In':
            matched = self.vision.find_template('find-match') or self.vision.find_template('find-match-free')
            #self.log(matched)
            time.sleep(0.5)
            if matched:
                self.log('Found Match In')
                self.controller.action_key('s', 0.2)
                section = 'Out'
            else :
                self.vision.refresh_frame()
                self.state = 'finding match'
        while section == 'Out':
            self.vision.refresh_frame()
            matched = self.vision.find_template('find-match') or self.vision.find_template('find-match-free')
            #self.log(matched)
            time.sleep(0.5)
            if matched:
                self.log('Found Match Out')
                self.controller.action_key('s', 0.2)
                section = 'Out'
            else :
                self.log('Out complete')
                section = 'Done'
                self.state = 'picking opponents'

    def pick_opponents(self):
        section = 'In'
        while section == 'In':
            matched = self.vision.find_template('continue')
            #self.log(matched)
            time.sleep(1)
            if matched:
                self.log('Found Match In')
                self.controller.action_key('d', 0.2)
                section = 'Out'
            else :
                self.vision.refresh_frame()
                self.state = 'picking opponents'
        while section == 'Out':
            self.vision.refresh_frame()
            matched = self.vision.find_template('continue')
            #self.log(matched)
            time.sleep(1)
            if matched:
                self.log('Found Match Out')
                self.controller.action_key('d', 0.2)
                section = 'Out'
            else :
                self.log('Out complete')
                section = 'Done'
                self.state = 'accepting config'
    
    def accept_config(self):
        section = 'In'
        while section == 'In':
            matched = self.vision.find_template('accept')
            #self.log(matched)
            if matched:
                self.log('Found Match In')
                self.controller.action_key('d', 0.2)
                section = 'Out'
            else :
                time.sleep(2)
                self.vision.refresh_frame()
                self.state = 'accepting config'
        while section == 'Out':
            time.sleep(2)
            self.vision.refresh_frame()
            matched = self.vision.find_template('accept')
            #self.log(matched)
            if matched:
                self.log('Found Match Out')
                self.controller.action_key('d', 0.2)
                section = 'Out'
            else :
                self.log('Out complete')
                section = 'Done'
                self.state = 'continuing to fight'

    def continue_to_fight(self):
        section = 'In'
        i=0
        self.log('in continue section')
        
        while section == 'In' and i < 10:
            matched = self.vision.find_template('continue')
            self.log(matched)
            time.sleep(1)
            i = i + 1
            if matched:
                self.log('Found Match In')
                self.controller.action_key('d', 0.2)
                section = 'Out'
                i = 0
            else :
                self.vision.refresh_frame()
                self.state = 'continuing to fight'
                if i == 10:
                    i = 0
                    section = 'Out'
        while section == 'Out' and i < 10:
            self.vision.refresh_frame()
            matched = self.vision.find_template('continue')
            self.log(matched)
            time.sleep(1)
            i = i + 1
            if matched:
                self.log('Found Match Out')
                self.controller.action_key('d', 0.2)
                section = 'Out'
                if i == 10:
                    self.state = 'loading into fight'
                    break
            else :
                self.log('Out complete')
                i = 0
                section = 'Done'
                self.state = 'loading into fight'

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
        section = 'In'
        while section == 'In':
            coord = self.vision.find_template_center('next-series')
            time.sleep(1)
            if coord:
                self.log('Found Match In')
                self.controller.click_button(coord[0], coord[1])
                time.sleep(1)
                section = 'Out'
            else:
                self.vision.refresh_frame()
                self.state = 'next series'
        while section == 'Out':
            self.vision.refresh_frame()
            coord = self.vision.find_template_center('next-series')
            time.sleep(1)
            if coord:
                self.log('Found Match Out')
                self.controller.click_button(coord[0], coord[1])
                time.sleep(1)
                section = 'Out'
            else:
                self.log('Out complete')
                section = 'Done'
                self.state = 'champ setup'

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))