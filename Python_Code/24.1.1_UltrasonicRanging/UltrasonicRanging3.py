# Filename: UltrasonicRanging3.py
# Project: Freenove kit using pigpio C and Python library
# Description: read from a HC SR04 ultrasonic ranging module
# Author: JudaV
# date: october 2024

import pigpio
import time

trigPin = 23  # define trigger pin and echo pin
echoPin = 24

# connect to raspberry pi IO pins:
pi = pigpio.pi()
high_tick = None
low_tick = None


def setup():
    pi.set_mode(echoPin, pigpio.INPUT)
    pi.set_pull_up_down(echoPin, pigpio.PUD_DOWN)
    pi.set_mode(trigPin, pigpio.OUTPUT)
    pi.set_glitch_filter(echoPin, 100)


def loop():
    while True:
        time.sleep(0.5)
        trigger()
        # catch change bij callback function
        pi.callback(echoPin, pigpio.EITHER_EDGE, receive_callback)
        time.sleep(1)


def receive_callback(gpio, level, tick):
    global high_tick, low_tick

    if level == 1:  # rising edge
        high_tick = tick
    else:
        low_tick = tick  # level 0 means falling edge
    if (high_tick is not None) and (low_tick is not None):
        pulse_time = pigpio.tickDiff(high_tick, low_tick)
        high_tick = None  # start new measurement
        low_tick = None
        if pulse_time < 10000:  # filter missed ticks
            # print(f"pulse_time: {pulse_time}")
            print(f"The distance is: {(340/2)* (pulse_time/10000):.2f}cm")
        time.sleep(1)


# start measuring cycle by raising trigger pin 10us
def trigger():
    pi.write(trigPin, 0)
    time.sleep(0.50)
    pi.write(trigPin, 1)
    time.sleep(0.00001)  # 10us
    pi.write(trigPin, 0)


def destroy():
    pi.stop()
    print(f"\nbye\n")


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
