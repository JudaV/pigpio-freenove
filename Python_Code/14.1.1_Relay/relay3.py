# Filename: Relay3.py
# Project: Freenove kit using pigpio C and Python library
# Description: use a relay module
# Author: JudaV
# date: october 2024

import pigpio
import time

button_pin = 18  # set button_pin vatiable to GPIO18
led_pin = 17  # define led_pin to BCM GPIO17
pi1 = pigpio.pi()  # Initialise Pi connection and access to the local Pi's GPIO
led_state = 0


def callback_function(gpio, level, tick):
    # print("button press detected")
    # print(gpio, level, tick)
    global led_state
    led_state = not led_state
    if led_state:
        pi1.write(17, 1)
        print("Led turned on", tick)

    else:
        print("Led turned off", tick)
        pi1.write(17, 0)


def setup():
    print("using pin %d and pin %d" % (led_pin, button_pin))
    pi1.set_glitch_filter(18, 50000)
    # pi1.set_noise_filter(18, 5000, 5000)

    pi1.read(18)
    pi1.write(17, 0)
    pi1.set_pull_up_down(18, pigpio.PUD_UP)  # set buttonPin to PULL UP INPUT mode


def loop():
    print("control-C to terminate")
    while True:
        pi1.wait_for_edge(18, pigpio.FALLING_EDGE, 300)
        callback1 = pi1.callback(18, pigpio.FALLING_EDGE, callback_function)
        time.sleep(0.05)


def destroy():
    pi1.write(17, 0)
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
