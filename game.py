import numpy as np
import time
import cv2
import tkinter as tk

class Game:
    # Use a time variable to do the individual states
    # Make curr time and last time
    # check for delta time
    # if its greater than the amount we want, do the state

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'game start'
        self.series = 0
        self.master = tk.Tk()
        self.counter = tk.IntVar()
        self.showstate = tk.StringVar()
        self.running = tk.BooleanVar()
        self.running.set(True)
        self.time1 = time.time()
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time2
        self.section = 'In'
        self.quitseries = False
        self.showstate.set(self.state)

    def onQuit(self, event=None):
        self.log('Stopping Script')
        self.running.set(False)
        #print(self.running.get())

    def quitLater(self):
        self.quitseries = True
        self.controller.click_on_window()
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

        # master = tk.Tk()
        self.master.geometry('200x100+500+800')
        self.master.title('Arena Script')

        self.master.grid_columnconfigure(0, minsize=100)
        self.master.grid_columnconfigure(1, minsize=100)
        quitnowbutton = tk.Button(self.master, text='Quit Now', command=self.onQuit)
        quitlaterbutton = tk.Button(self.master, text='Quit After Series', command=self.quitLater)
        quitnowbutton.grid(row=0, column=0, columnspan=1, sticky=tk.W + tk.E)
        #quitnowbutton.pack()
        quitlaterbutton.grid(row=1, column=0, columnspan=1, sticky=tk.W + tk.E)
        #quitlaterbutton.pack()
        seriestitle = tk.Label(self.master, text=' Series Count ')
        seriescount = tk.Label(self.master, textvariable=self.counter)
        shownstate = tk.Label(self.master, textvariable=self.showstate)
        seriestitle.grid(row=0, column=1)
        #seriestitle.pack()
        seriescount.grid(row=1, column=1)
        shownstate.grid(row=3, column=0)
        #seriescount.pack()

        while self.running.get():
            self.showstate.set(self.state)
            self.master.update_idletasks()
            self.master.update()
            if self.state == 'game start':
                self.game_start()
            elif self.state == 'champ setup':
                self.champ_setup()
            elif self.state == 'finding match':
                self.find_match()
            elif self.state == 'picking opponents':
                self.pick_opponents()
            elif self.state == 'accepting config':
                self.accept_config()
            elif self.state == 'continuing to fight':
                self.continue_to_fight()
            elif self.state == 'loading into fight':
                self.load_into_fight()
            elif self.state == 'fighting':
                self.fighting()
            elif self.state == 'next fight':
                self.next_fight()
            elif self.state == 'final fight':
                self.final_fight()
            elif self.state == 'ending match':
                self.end_match()
            elif self.state == 'next series':
                self.next_series()                      
            else:
                pass
            #time.sleep(1)

    def game_start(self):
        self.log('Script Startup')
        self.controller.click_on_window()
        self.state = 'champ setup'

    # Check if there is an X
    # If so, press X
    # If no check for help
    # If no check for empty slot
    # If none of these are triggered, move on

    def champ_setup(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        # self.log(self.deltatime)
        if self.deltatime > 2:
            # self.log(self.deltatime)
            self.vision.refresh_frame()
            matchedhelp = self.vision.find_template('help-button')
            matchedempty = self.vision.find_template('empty-slot-bottom')
            matchedinfo = self.vision.find_template('info')
            # matchedexit = self.vision.find_template('exit')
            if matchedinfo:
                self.log('Click out of champ info')
                self.controller.click_button(156, 500)
            elif matchedhelp:
                self.log('Ask for help')
                self.controller.action_key('h', 0.5)
            elif matchedempty:
                self.log('Insert Champ')
                self.controller.action_key('a', 0.5)
            else:
                self.state = 'finding match'
                # self.state = 'debug'
                # self.log('Stopped')
            self.time1 = time.time()

    # Create states in each method. In and Out states            

    def find_match(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 5:
            if self.section == 'In':
                self.vision.refresh_frame()
                matched = self.vision.find_template('find-match') or self.vision.find_template('find-match-free') or self.vision.find_template('find-match-2000')
                if matched:
                    self.log('Finding Match')
                    self.controller.action_key('s', 0.2)
                    self.section = 'Out'
                else:
                    self.state = 'finding match'
            elif self.section == 'Out':
                self.vision.refresh_frame()
                matched = self.vision.find_template('find-match') or self.vision.find_template('find-match-free') or self.vision.find_template('find-match-2000')
                if matched:
                    self.controller.action_key('s', 0.2)
                else:
                    self.log('Found Match')
                    self.state = 'picking opponents'
                    self.section = 'In'
            self.time1 = time.time()

    def pick_opponents(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 5:
            if self.section == 'In':
                self.vision.refresh_frame()
                matched = self.vision.find_template('continue')
                if matched:
                    self.log('Picking Opponents')
                    self.controller.action_key('d', 0.2)
                    self.section = 'Out'
                else:
                    self.state = 'picking opponents'
            elif self.section == 'Out':
                self.vision.refresh_frame()
                matched = self.vision.find_template('continue')
                if matched:
                    self.controller.action_key('d', 0.2)
                else:
                    self.log('Opponents Picked')
                    self.state = 'accepting config'
                    self.section = 'In'
            self.time1 = time.time()

    def accept_config(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 5:
            if self.section == 'In':
                self.vision.refresh_frame()
                matched = self.vision.find_template('accept')
                if matched:
                    self.log('Accepting Champ configuration')
                    self.controller.action_key('d', 0.2)
                    self.section = 'Out'
                else:
                    self.state = 'accepting config'
            elif self.section == 'Out':
                self.vision.refresh_frame()
                matched = self.vision.find_template('accept')
                if matched:
                    self.controller.action_key('d', 0.2)
                else:
                    self.log('Accepted configuration')
                    self.state = 'continuing to fight'
                    self.section = 'In'
            self.time1 = time.time()

    def continue_to_fight(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 5:
            self.log('in continue section')
            if self.section == 'In':
                self.vision.refresh_frame()
                matched = self.vision.find_template('continue')
                if matched:
                    self.log('Continuing to fight')
                    self.controller.action_key('d', 0.2)
                    self.section = 'Out'
                else:
                    self.state = 'continuing to fight'
            elif self.section == 'Out':
                self.vision.refresh_frame()
                matched = self.vision.find_template('continue')
                if matched:
                    self.controller.action_key('d', 0.2)
                else:
                    self.log('Loading into fight')
                    self.state = 'loading into fight'
                    self.section = 'In'                   
            self.time1 = time.time()

    def load_into_fight(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 0.05:
            self.vision.refresh_frame()
            matched = self.vision.find_template('pause')
            if matched:
                self.log('Begin fighting')
                self.state = 'fighting'
            else:
                self.state = 'loading into fight'
            self.time1 = time.time()

    def fighting(self):
        self.vision.refresh_frame()
        matched = self.vision.find_template('pause')
        if matched:
            #self.log('Found pause')
            self.controller.action_key('g', 0.05)
            self.controller.action_key('f', 0.01)
            self.controller.action_key('f', 0.01)
            self.controller.action_key('f', 0.01)
            self.controller.action_key('f', 0.01)
            self.controller.action_key('a', 0.01)
            self.controller.action_key('s', 0.01)
            self.state = 'fighting'
        else:
            self.log('Fight End')
            self.state = 'next fight'
        self.time1 = time.time()

    def next_fight(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 10:
            self.vision.refresh_frame()
            matched = self.vision.find_template('next-fight')
            matched2 = self.vision.find_template('final-fight')
            matched3 = self.vision.find_template('end-match')
            if matched:
                self.controller.action_key('j')
                self.controller.action_key('k')
                self.log('Loading into second fight')
                self.state = 'loading into fight'
            elif matched2:
                self.controller.action_key('j')
                self.controller.action_key('k')
                self.log('Loading into final fight')
                self.state = 'loading into fight'
            elif matched3:
                self.controller.action_key('j')
                self.controller.action_key('k')
                self.log('Exiting fight')
                self.state = 'next series'
            else:
                self.state = 'next fight'
            self.time1 = time.time()

    def next_series(self):
        self.time2 = time.time()
        self.deltatime = self.time2 - self.time1
        if self.deltatime > 12:
            if self.section == 'In':
                self.vision.refresh_frame()
                coord = self.vision.find_template_center('next-series')
                if coord:
                    self.log('Going to next series')
                    self.controller.click_button(coord[0], coord[1])
                    self.section = 'Out'
                else:
                    self.state = 'next series'
            elif self.section == 'Out':
                self.vision.refresh_frame()
                coord = self.vision.find_template_center('next-series')
                if coord:
                    self.controller.click_button(coord[0], coord[1])
                else:
                    self.counter.set(self.counter.get() + 1)
                    self.log('Begin next series')
                    self.state = 'champ setup'
                    self.section = 'In'
                    if self.quitseries is True:
                        self.onQuit()
            self.time1 = time.time()

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
