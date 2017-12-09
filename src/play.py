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
    opts, _ = getopt.getopt(argv, "d:")
    soundsPath = "../sound"
    for opt, arg in opts:
        if opt == "-d":
            soundsPath = arg
    pygame.init()
    pygame.mixer.init()            
    random.seed(datetime.now())
    fList = glob.glob(os.path.join(soundsPath, '*.mp3'))
    brd = board.Board(fList = fList)
    brd.run()
                
        
if __name__ == '__main__':
    main(sys.argv[1:])
