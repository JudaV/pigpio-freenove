# Filename: softlight3.py
# Project: Freenove kit using pigpio C and Python library
# Description: use of 8591 ADC chip to control the color of RGBLED with potentiometers
# Author: JudaV
# date: october 2024

import time
import curses
import pigpio

# sudo pigpiod
# Connect Pi 3V3 - VCC, Ground - Ground, SDA - SDA, SCL - SCL.

YL_40 = 0x48
aout = 0
pi = pigpio.pi()  # Connect to local Pi
handle = pi.i2c_open(1, YL_40, 0)
stdscr = curses.initscr()
pins = [22, 27, 17, 13]  # 13 used as dummy


def setup():
    curses.noecho()
    curses.cbreak()
    stdscr.addstr(10, 0, "RED")
    stdscr.addstr(12, 0, "GREEN")
    stdscr.addstr(14, 0, "BLUE")
    stdscr.addstr(16, 0, "Resistor")
    stdscr.nodelay(1)

    pi.set_PWM_frequency(22, 20000)
    pi.set_PWM_frequency(27, 20000)
    pi.set_PWM_frequency(17, 20000)
    pi.set_PWM_dutycycle(22, 0)
    pi.set_PWM_dutycycle(27, 0)
    pi.set_PWM_dutycycle(17, 0)


def loop():
    while True:
        for a in range(0, 4):
            # AIN0 connected red adress 0x04 AIN1= 0x05, connects green etc
            global aout
            aout = aout + 1
            pi.i2c_write_byte_data(handle, 0x40 | ((a + 1) & 0x03), aout & 0xFF)
            v = pi.i2c_read_byte(handle)
            pi.set_PWM_dutycycle(pins[a], v)
            time.sleep(0.04)

            hashes = int(v / 4)
            spaces = 64 - hashes
            stdscr.addstr(10 + a * 2, 12, str(v) + " ")
            stdscr.addstr(10 + a * 2, 16, "#" * hashes + " " * spaces)

        stdscr.refresh()
        c = stdscr.getch()

        if c != curses.ERR:
            break


def destroy():
    curses.nocbreak()
    curses.echo()
    curses.endwin()

    pi.i2c_close(handle)
    pi.write(22, 1)
    pi.write(27, 1)
    pi.write(17, 1)
    pi.stop()
    print("bye")


if __name__ == "__main__":
    print("Program is starting ... ")
    setup()
    loop()
    destroy()
