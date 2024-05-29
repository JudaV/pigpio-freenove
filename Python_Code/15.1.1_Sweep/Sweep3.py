import pigpio
import time
 
pin_18 = 18            # set pin_18 variable to GPIO18
pi = pigpio.pi()       # Initialise Pi connection and access to the local Pi's GPIO

def setup():
    pi.set_PWM_frequency(pin_18, 50)
    pi.set_PWM_range(pin_18, 1000)    # set range 1000, so that zero degrees is 25 and 180 deg is 125 /1000
    print ("using pin %d", (pin_18))

def loop():
    while True:
        for i in range(25,125):
            pi.set_PWM_dutycycle(pin_18, i)
            time.sleep(0.01)
        time.sleep(0.5)
        for i in range(125, 24, -1):
            pi.set_PWM_dutycycle(pin_18, i)
            time.sleep(0.01)
        time.sleep(0.5)


def destroy():
    pi.stop()                       # Release all GPIO
    print("program terminated")


if __name__ == '__main__':           # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")
        
    finally:
        destroy()
