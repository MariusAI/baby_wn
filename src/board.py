import RPi.GPIO as GPIO
import time
import threading
import pygame
import random

class Board:
    def __init__(self, fList=[], inputs={}):
        GPIO.setmode(GPIO.BOARD)
        random.seed(time.time())
        self.fList = fList
        self.inputs = {}
        self.playBtn = 11
        self.stopBtn = 12
        self.ledOut = 16
        self.volDownBtn = 13
        self.volUpBtn = 15
        self.pull = GPIO.PUD_UP
        GPIO.setup(self.playBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.stopBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.volUpBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.volDownBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.ledOut, GPIO.OUT)
        self.playEvent = threading.Event()
        self.stopEvent = threading.Event()
        self.volUpEvent = threading.Event()
        self.volDownEvent = threading.Event()
        self.state = {self.volDownBtn: 1,
                      self.volUpBtn: 1,
                      self.stopBtn: 1,
                      self.playBtn: 1}
        self.events = {self.volDownBtn: self.volDownEvent,
                       self.volUpBtn: self.volUpEvent,
                       self.stopBtn: self.stopEvent,
                       self.playBtn: self.playEvent}
        self.killpill = threading.Event()
        self.keydelay = 0.001 # 0.001

    def volumeUp(self):
        while True:
            if self.killpill.is_set():
                return
            self.events[self.volUpBtn].wait(1)
            if self.events[self.volUpBtn].is_set():
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(min(1.0, vol + 0.05))
                # print pygame.mixer.music.get_volume()
                self.events[self.volUpBtn].clear()

    def volumeDown(self):
        while True: 
            if self.killpill.is_set():
                return
            self.events[self.volDownBtn].wait(1)
            if self.events[self.volDownBtn].is_set():
                vol = pygame.mixer.music.get_volume()
                pygame.mixer.music.set_volume(max(0.0, vol - 0.05))
                # print pygame.mixer.music.get_volume()
                self.events[self.volDownBtn].clear()

                
    def playMP3(self):
        while True:
            if self.killpill.is_set():
                return
            time.sleep(1)
            if not self.events[self.playBtn].is_set():
                continue
            if len(self.fList) > 0:
                random.shuffle(self.fList)
                pygame.mixer.music.load(self.fList[0])
                pygame.mixer.music.play()
            while self.events[self.playBtn].wait(0.01) or self.events[self.stopBtn].wait(0.01):
                time.sleep(0.001)
            pygame.mixer.music.stop()
            

    def run(self):
        self.threads = {'play': threading.Thread(target=self.playMP3),
                        'volUp': threading.Thread(target = self.volumeUp),
                        'volDown': threading.Thread(target = self.volumeDown),
        }
                        #'volDown': None}
        for k in self.threads:
            self.threads[k].start()
        try:
            while True:
                time.sleep(self.keydelay)
                # read button state
                switched = self.readButtons()
                for k in switched.keys():
                    if switched[k]:
                        if self.events[k].is_set():
                            self.events[k].clear()
                            # print "Cleared event %d." % k
                        else:
                            self.events[k].set()
                            # print "Set event %d." % k
        except Exception as e:
            print e
            self.killpill.set()
            for k in self.threads:
                self.threads[k].join()            

            
    def readButtons(self):
        new_state = dict(self.state)
        outputs = dict(self.state)
        for k in self.state.keys():
            new_state[k] = GPIO.input(k)
            outputs[k] = (new_state[k] == 0) and (new_state[k] != self.state[k])
        self.state = new_state
        # print self.state, outputs
        return outputs
    
    def getPlayButton(self):
        return GPIO.input(self.playBtn)

    def setLED(self, flag):
        if flag:
            flag = 1
        else:
            flag = 0
        GPIO.output(self.ledOut, flag)
    
    def readState(self):
        return (GPIO.input(self.playBtn))
