#1/usr/bin/python

import pygame
import sys
import os
import getopt
import glob
import random
from datetime import datetime
import threading
import time
import board
import RPi.GPIO as GPIO

# def playMP3(fList, stop_event):
#     while True:
#         random.shuffle(fList)
#         pygame.mixer.music.load(fList[0])
#         pygame.mixer.music.play()
#         # while pygame.mixer.music.get_busy():
#         for k in range(100):
#             time.sleep(1)
#             if stop_event.wait(1):
#                 pygame.mixer.music.stop()
#                 return

def main(argv):
    opts, _ = getopt.getopt(argv, "d:l:")
    soundsPath = "../sound"
    logFile = None
    for opt, arg in opts:
        if opt == "-d":
            soundsPath = arg
        elif opt == '-l':
            logFile = arg
    pygame.init()
    pygame.mixer.init()            
    random.seed(datetime.now())
    fList = glob.glob(os.path.join(soundsPath, '*.mp3'))
    brd = board.Board(fList = fList, logFile=logFile)
    player_thread=threading.Thread(target=brd.manage_player)
    try:
        player_thread.start()
        player_thread.join()
    except:
        print("received KeyboardInterrupt")
        brd.killpill.set()
        print("Set the killpill")
        player_thread.join()
        GPIO.cleanup()
    GPIO.cleanup()
        
        
        
if __name__ == '__main__':
    main(sys.argv[1:])
