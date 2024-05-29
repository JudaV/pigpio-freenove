import pigpio
import math
import time

button_pin = 18         # set button_pin variable to GPIO18
buzz_pin = 17           # define buzz_pin to BCM GPIO17
pi1 = pigpio.pi()       # Initialise Pi connection and access to the local Pi's GPIO


def alertor():
    for x in range(0,361):      # Make frequency of the alertor consistent with the sine wave
        sinVal = math.sin(x * (math.pi / 180.0))        # calculate the sine value
        toneVal = int(2000 + sinVal * 500)   # Add to the resonant frequency with a Weighted
        pi1.set_PWM_frequency(buzz_pin,toneVal)      # Change Frequency of PWM to toneVal
        
        time.sleep(0.001)

def setup():
    pi1.set_pull_up_down(button_pin, pigpio.PUD_UP)
    print ('using pin %d and pin %d' % (buzz_pin, button_pin))

def loop():
    while True:
        if pi1.read(button_pin) == 0:
            pi1.set_PWM_dutycycle(buzz_pin, 255) # PWM full on
            alertor()
            print ('alertor turned on >>> ')
        else :
            pi1.write(buzz_pin,0)
            print ('alertor turned off <<<')


def destroy():
    pi1.stop()                       # Release all GPIO
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
