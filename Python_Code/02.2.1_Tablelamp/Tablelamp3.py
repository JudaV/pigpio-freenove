# Filename: Tablelamp3.py
# Project: Freenove kit using pigpio C and Python library
# Description: Use a button to control a LED
# Author: JudaV
# date: october 2024

import pigpio

button_pin = 18  # set button_pin vatiable to GPIO18
led_pin = 17  # define led_pin to BCM GPIO17
pi1 = pigpio.pi()  # Initialise Pi connection and access to the local Pi's GPIO


def setup():
    print("using pin %d and pin %d" % (led_pin, button_pin))
    pi1.read(18)
    pi1.write(17, 0)
    pi1.set_pull_up_down(18, pigpio.PUD_UP)  # set buttonPin to PULL UP INPUT mode


def loop():
    while True:
        led_state = pi1.read(17)  # capture whether LED is on
        if pi1.wait_for_edge(18, pigpio.FALLING_EDGE, 3600):
            print("button press detected")
            led_state = not led_state
            if led_state:
                pi1.write(17, 1)
                print("Led turned on")
            else:
                print("Led turned off")
                pi1.write(17, 0)
        else:
            pass


def destroy():
    pi1.stop()  # Release all GPIO
    print("program terminated\n")


if __name__ == "__main__":  # Program entrance
    print("Program is starting\n")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("\nKeyboard Interrupt\n")
    finally:
        destroy()
