# Filename: LightWater3.py
# Project: Freenove kit using pigpio C and Python library
# Description: use LED-bar
# Author: JudaV
# date: october 2024

import pigpio
import time


pins = [17, 18, 27, 22, 23, 24, 25, 2, 3, 8]
pi1 = pigpio.pi()  # Initialise Pi connection and access to the local Pi's GPIO


def setup():
    for _ in pins:
        pi1.write(_, 1)


def loop():
    while True:
        for pin in pins:  # make led(on) move from left to right
            pi1.write(pin, 0)
            time.sleep(1)
            pi1.write(pin, 1)
        for pin in pins[::-1]:  # make led(on) move from right to left
            pi1.write(pin, 0)
            time.sleep(1)
            pi1.write(pin, 1)


def destroy():
    pi1.stop()  # Release all GPIO
    print("program terminated\n")


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
