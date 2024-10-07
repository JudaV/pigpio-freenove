# Filename: Senseled3.py
# Project: Freenove kit using pigpio C and Python library
# Description: read from a infrared pyroelectric sensor
# Author: JudaV
# date: october 2024


import pigpio

ledPin = 18  # define ledPin
sensorPin = 17  # define sensorPin

# connect to raspberry pi IO pins:
pi = pigpio.pi()


def setup():
    pi.set_mode(sensorPin, pigpio.INPUT)
    pi.set_pull_up_down(sensorPin, pigpio.PUD_DOWN)
    pi.set_mode(ledPin, pigpio.OUTPUT)


def loop():
    while True:
        if pi.read(sensorPin):  # if sensor read is high
            pi.write(ledPin, 1)
        else:
            pi.write(ledPin, 0)


def destroy():
    pi.write(ledPin, 0)
    pi.stop()
    print(f"\nbye\n")


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
