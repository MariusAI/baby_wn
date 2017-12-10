import RPi.GPIO as GPIO
import time
import threading
import pygame
import random
import logging

class Board:
    def __init__(self, fList=[], inputs={}, logFile=None):
        self.logFile = logFile
        # self.logger = self.createLogger()
        logging.basicConfig(filename=self.logFile,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        GPIO.setmode(GPIO.BOARD)
        random.seed(time.time())
        self.fList = fList
        self.inputs = {}
        self.playBtn = 11
        self.stopBtn = 12
        self.ledOut = 16
        self.volDownBtn = 13
        self.volUpBtn = 15
        # set the volume
        pygame.mixer.music.set_volume(0.5)
        self.pull = GPIO.PUD_UP
        GPIO.setup(self.playBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.stopBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.volUpBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.setup(self.volDownBtn, GPIO.IN, pull_up_down=self.pull)
        GPIO.add_event_detect(self.volUpBtn,
                              GPIO.FALLING,
                              callback=self.turnVolUp,
                              bouncetime=25)
        GPIO.add_event_detect(self.volDownBtn,
                              GPIO.FALLING,
                              callback=self.turnVolDown,
                              bouncetime=25)
        GPIO.setup(self.ledOut, GPIO.OUT)
        self.playing = False
        self.killpill = threading.Event()
        self.keydelay = 0.001 # 0.001                random.shuffle(self.fList)

    def createLogger(self):
        self.logger = logging.getLogger('baby_wn')
        self.logger.setLevel(logging.ERROR)
        if self.logFile is None:
            fh = logging.StreamHandler()
        else:
            fh = logging.FileHandler(self.logFile)
        fh.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        return self.logger
            
    def turnVolUp(self, channel):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(min(1.0, vol + 0.05))
        logging.info("Set the volume to {}".format(vol))
        
    def turnVolDown(self, channel):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(max(0.0, vol - 0.05))
        logging.info("Set the volume to {}".format(vol))

    def startMP3(self, fList):

        if len(fList) > 0:
            ch = None
            while ch is None:
                random.shuffle(fList)
                pygame.mixer.music.load(fList[0])
                logging.info("Playing file '{}'".format(fList[0]))
                pygame.mixer.music.play()
                while ch is None:
                    ch = GPIO.wait_for_edge(self.playBtn, GPIO.FALLING, timeout=1000, bouncetime=500)
                    if self.killpill.is_set():
                        logging.info("'startMP3' received the killpill")
                        pygame.mixer.music.stop()
                        return
                    if not pygame.mixer.music.get_busy():
                        break
            pygame.mixer.music.stop()

    def manage_player(self):
        while True:
            logging.info("Waiting for play commands...")
            ch = GPIO.wait_for_edge(self.playBtn, GPIO.FALLING, bouncetime=500)
            self.startMP3(self.fList)
            if self.killpill.is_set():
                logging.info("Received the killpill")
                return
            
