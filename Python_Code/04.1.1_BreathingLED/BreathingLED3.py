import pigpio
import time

led_pin = 17            # define the LedPin
pi1 = pigpio.pi()      # Initialise Pi connection and access to the local Pi's GPIO

def setup():
    pi1.set_PWM_dutycycle(led_pin, 0) # starts PWM at zero
    pi1.set_PWM_range(led_pin, 100)   # sets the maximum at 100(%)

def loop():
    while True:
        for dc in range(0, 101, 1):   # make the led brighter
            pi1.set_PWM_dutycycle(led_pin, dc)     # set dc value as the duty cycle
            time.sleep(0.01)
        time.sleep(1)
        for dc in range(100, -1, -1): # make the led darker
            pi1.set_PWM_dutycycle(led_pin, dc)     # set dc value as the duty cycle
            time.sleep(0.01)
        time.sleep(1)


def destroy():
    pi1.stop()                       # Release all GPIO
    print("\nprogram terminated\n")


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
