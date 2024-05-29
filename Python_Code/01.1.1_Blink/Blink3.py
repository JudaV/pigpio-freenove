import pigpio
import time


ledPin = 17             # define ledPin to BCM GPIO17
pi1 = pigpio.pi()       # pi1 accesses the local Pi's GPIO


def setup():
    print ('using pin%d' %ledPin)


def loop():
    while True:
        pi1.write(ledPin, 0)         # set local Pi's GPIO 4 low
        print ('led turned off')     # print information on terminal
        time.sleep(3)                # Wait for 3 second
        pi1.write(ledPin, 1)         # make ledPin output LOW level to turn off led
        print ('led turned on')
        time.sleep(1)                # Wait for 1 second


def destroy():
    pi1.stop()                       # Release all GPIO


if __name__ == '__main__':           # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\n program stopped by Keyboard Interrupt")
        
    finally:
        destroy()