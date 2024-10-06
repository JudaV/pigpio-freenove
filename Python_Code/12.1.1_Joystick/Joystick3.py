# Filename: Joystick3.py
# Project: Freenove kit using pigpio C and Python library
# Description: use of 8591 ADC chip to read a joystick
# Author: JudaV
# date: october 2024

import time
import curses
import pigpio


Z_Pin = 18  # define Z_Pin
YL_40 = 0x48
aout = 0
pi = pigpio.pi()  # Connect to local Pi
handle = pi.i2c_open(1, YL_40, 0)
stdscr = curses.initscr()


def setup():
    pi.set_pull_up_down(Z_Pin, pigpio.PUD_UP)
    curses.noecho()
    curses.cbreak()
    stdscr.addstr(10, 0, "X-Axis")
    stdscr.addstr(12, 0, "Y- Axis")
    stdscr.addstr(14, 0, "Z-Axis")
    stdscr.addstr(16, 0, " ")
    stdscr.nodelay(1)


def loop():
    while True:
        for a in range(0, 4):
            # AIN0 connected red adress 0x04 AIN1= 0x05, connects green etc
            global aout
            aout = aout + 1
            pi.i2c_write_byte_data(handle, 0x40 | ((a + 1) & 0x03), aout & 0xFF)
            v = pi.i2c_read_byte(handle)
            time.sleep(0.04)

            time.sleep(0.01)
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
    pi.stop()
    print("bye")


if __name__ == "__main__":
    print("Program is starting ... ")
    setup()
    loop()
    destroy()
