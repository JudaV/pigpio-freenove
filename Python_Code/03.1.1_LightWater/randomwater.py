#!/usr/bin/env python3
#######################################################################
# Filename    : LightWater.py
# Description : Use LEDBar Graph(10 LED)
# auther      : www.freenove.com
# modification: 2019/12/28
########################################################################
import RPi.GPIO as GPIO
import time
import random

ledPins = [11, 12, 13, 15, 16, 18, 22, 3, 5, 24]


def setup():
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPins, GPIO.OUT)   # set all ledPins to OUTPUT mode
    GPIO.output(ledPins, GPIO.HIGH)  # make all ledPins output HIGH level, turn off all led


def loop():
    while True:
        try:
            getal = input("geef een getal tussen 1 en 10:   ")
            rand = int(getal)
        except:
            print("das nie goe")
        # rand = random.randint(1,10)
        # print(rand)
        for pin in ledPins[:rand]:     # make led(on) move from left to right
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(pin, GPIO.HIGH)
        for pin in ledPins[-(11-rand)::-1]:  # make led(on) move from right to left
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.2)
            GPIO.output(pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(ledPins, GPIO.HIGH)
        GPIO.output(ledPins[0:rand], GPIO.LOW)
        time.sleep(1)
        GPIO.output(ledPins, GPIO.HIGH)


def destroy():
    GPIO.cleanup()                     # Release all GPIO


if __name__ == '__main__':     # Program entrance
    print('Haan met die bwanaan...')

    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
