# Filename: StopWatch3.py
# Project: Freenove kit using pigpio C and Python library
# Description: control a 4-digit 7-segment display with a 74HC595 shift register
# Author: JudaV
# date: october 2024

import time
import threading
import pigpio

pi = pigpio.pi()

data_pin = 24  # connected to DS (14 on the IC)  - Serial data Input
latch_pin = 23  # connected to ST-CP (12 on the IC)  - Parallel update output:
#     when its electrical level is rising,
#     it will update the parallel data output.
clock_pin = 18  # connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is
# rising, serial data input register will do a shift.
pins_to_shift = [data_pin, latch_pin, clock_pin]
digitPins = (17, 27, 22, 10)  # Define the pin of 7-segment display common end

LSBFIRST = 1
MSBFIRST = 2

# numbers zero to nine to be displayed
num = (0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8, 0x80, 0x90)

counter = 0  # Variable counter which will be dislayed by 7-segment display
t = 0  # define the Timer object


def setup():
    for pin in pins_to_shift:
        pi.set_mode(pin, pigpio.OUTPUT)
    for pin in digitPins:
        pi.set_mode(pin, pigpio.OUTPUT)


def shift_out(byte, order=MSBFIRST):  # default is MSBFIRST
    if order == MSBFIRST:  # default in this script
        for i in range(7, -1, -1):
            pi.write(clock_pin, 0)
            pi.write(
                data_pin, byte >> i & 1
            )  # rightshift value and bitmask 1 gives the last bit
            pi.write(clock_pin, 1)
    else:  #  LSBFIRST
        for i in range(0, 8):
            pi.write(clock_pin, 0)
            pi.write(
                data_pin, byte >> i & 1
            )  # rightshift value and bitmask 1 gives the last bit
            pi.write(clock_pin, 1)


def outData(data):  # function used to output data for 74HC595
    pi.write(latch_pin, 0)
    shift_out(data)
    pi.write(latch_pin, 1)


def selectDigit(digit):  # Open one of the 7-segment display and close the others
    if digit == 0:
        pi.write(digitPins[0], 0)
        for i in [1, 2, 3]:
            pi.write(digitPins[i], 1)
    elif digit == 1:
        pi.write(digitPins[1], 0)
        for i in [0, 2, 3]:
            pi.write(digitPins[i], 1)
    elif digit == 2:
        pi.write(digitPins[2], 0)
        for i in [0, 1, 3]:
            pi.write(digitPins[i], 1)
    else:
        pi.write(digitPins[3], 0)
        for i in [0, 1, 2]:
            pi.write(digitPins[i], 1)


def display(dec):  # display function for 7-segment display
    outData(0xFF)  # eliminate residual display
    selectDigit(3)  # Select the first, and display the single digit
    outData(num[dec % 10])
    time.sleep(0.0003)  # display duration
    outData(0xFF)
    selectDigit(2)  # Select the second, and display the tens digit
    outData(num[dec % 100 // 10])
    time.sleep(0.0003)
    outData(0xFF)
    selectDigit(1)  # Select the third, and display the hundreds digit
    outData(num[dec % 1000 // 100])
    time.sleep(0.0003)
    outData(0xFF)
    selectDigit(0)  # Select the fourth, and display the thousands digit
    outData(num[dec % 10000 // 1000])
    time.sleep(0.0003)


def timer():
    global counter
    global t
    t = threading.Timer(1.0, timer)  # reset time of timer to 1s
    t.start()  # Start timing
    counter += 1
    print(f"counter : {counter}")
    print("counter: %d" % counter)


def loop():
    global t
    global counter
    t = threading.Timer(1.0, timer)  # set the timer
    t.start()  # Start timing
    while True:
        display(counter)  # display the number counter


def clear_leds():
    """end the program with leds off: if the digitpins are low, leds will be off.
    for this the base in the PNP transistors are set to high: 1
    """
    for pin in digitPins:
        pi.write(pin, 1)


def destroy():
    global t
    t.cancel()
    clear_leds()
    pi.stop()
    print("\nprogram terminated\n")


if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("keyboard interrupt")
    finally:
        destroy()
