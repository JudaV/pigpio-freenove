
# Filename: softlight3.py
# Project: Freenove kit using pigpio C and Python library
# Description: smbus + use 8591 ADC chip to control LED with potentiometer
# Author: JudaV
# date: october 2024


import smbus
import time
import curses
import pigpio

# 2014-08-26 PCF8591-x.py

# Connect Pi 3V3 - VCC, Ground - Ground, SDA - SDA, SCL - SCL.

# ./PCF8591-x.py

bus = smbus.SMBus(1)
pi = pigpio.pi()
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
 
    for a in range(0,4):
        aout = aout + 1
        # bus.write_byte_data(0x48,0x40 | ((a+1) & 0x03), aout)
        bus.write_byte_data(0x48,0x40 | (0x4), aout)
        v = bus.read_byte(0x48)
        # hashes = v / 4
        # spaces = 64 - hashes
        stdscr.addstr(10, 12, str(v) + ' ')
        # stdscr.addstr(10+a*2, 16, '#' * hashes + ' ' * spaces )

    stdscr.refresh()
    time.sleep(0.04)
    pi.set_PWM_dutycycle(17,v)
    c = stdscr.getch()

    if c != curses.ERR:
        break


curses.nocbreak()
curses.echo()
curses.endwin()
pi.write(17,0)
pi.stop()