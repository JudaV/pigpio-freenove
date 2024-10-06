# Filename: softlight3.py
# Project: Freenove kit using pigpio C and Python library
# Description: use 8591 ADC chip to control LED with potentiometer
# Author: JudaV
# date: october 2024

import time
import curses
import pigpio

# sudo pigpiod
# ./PCF8591.py

# Connect Pi 3V3 - VCC, Ground - Ground, SDA - SDA, SCL - SCL.

YL_40 = 0x48
pi = pigpio.pi()  # Connect to local Pi.
handle = pi.i2c_open(1, YL_40, 0)
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
aout = 0

stdscr.addstr(10, 0, "Brightness")
# stdscr.addstr(12, 0, "Temperature")
# stdscr.addstr(14, 0, "AOUT->AIN2")
# stdscr.addstr(16, 0, "Resistor")
stdscr.nodelay(1)

while True:
    for a in range(0, 4):
        aout = aout + 1
        # pi.i2c_write_byte_data(handle, 0x40 | ((a+1) & 0x03), aout&0xFF)
        pi.i2c_write_byte_data(handle, 0x40 | (0x04), aout & 0xFF)
        v = pi.i2c_read_byte(handle)
        # hashes = v / 4
        # spaces = 64 - hashes
        stdscr.addstr(10, 12, str(v) + " ")
        # stdscr.addstr(10+a*2, 16, '#' * hashes + ' ' * spaces )

    stdscr.refresh()
    time.sleep(0.04)
    pi.set_PWM_dutycycle(17, v)
    c = stdscr.getch()
    if c != curses.ERR:
        break

curses.nocbreak()
curses.echo()
curses.endwin()

pi.i2c_close(handle)
pi.write(17, 0)
pi.stop()
print("bye")
