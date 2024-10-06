# Filename: BreathingLED3.py
# Project: Freenove kit using pigpio C and Python library
# Description: imitate candle light with random 
# Author: JudaV
# date: october 2024

import random, time
import RPi.GPIO as GPIO

led = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led, GPIO.OUT)

pwm = GPIO.PWM(led, 100)
RUNNING = True


def brightness():
    return random.randint(5, 100)


def flicker():
    return random.random() / 8


print("Stop -> CTRL + C")

try:
    while RUNNING:
        pwm.start(0)
        pwm.ChangeDutyCycle(brightness())
        time.sleep(flicker())
except KeyboardInterrupt:
    running = False
finally:
    pwm.stop()
    GPIO.cleanup()
