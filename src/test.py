import threading
import time
import board


def doit(arg):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        print ("working on %s" % arg)
        time.sleep(1)
    print("Stopping as you wish.")


def main():
#    t = threading.Thread(target=doit, args=("task",)) 
#    t.start()
#    time.sleep(1)
#    t.do_run = False
#    t.join()
    b = board.Board()
    while True:
        time.sleep(1)
        b.setLED(b.getPlayButton())
    
if __name__ == "__main__":
    main()
