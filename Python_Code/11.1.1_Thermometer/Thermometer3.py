import time
import curses
import pigpio
import math

YL_40=0x48
pi = pigpio.pi() # Connect to local Pi.
handle = pi.i2c_open(1, YL_40, 0)
 
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
aout = 0

stdscr.addstr(10, 0, "Temperature")
# stdscr.addstr(12, 0, "Temperature")
# stdscr.addstr(14, 0, "AOUT->AIN2")
# stdscr.addstr(16, 0, "Resistor")

stdscr.nodelay(1)

while True:
    for a in range(0,4):
        aout = aout + 1
        #pi.i2c_write_byte_data(handle, 0x40 | ((a+1) & 0x03), aout&0xFF)
        pi.i2c_write_byte_data(handle, 0x40 | (0x07), aout&0xFF) #connected to AIN3 at addsress 0x07
        v = pi.i2c_read_byte(handle)
        
        voltage = v / 255.0 * 3.3        # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
        tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)
        tempC = tempK -273.15        # calculate temperature (Celsius)
        string = ('ADC Value : %d, Voltage : %.2f, Temperature : %.2f'%(v,voltage,tempC))

        stdscr.addstr(10, 12, str(string) + ' ')

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
pi.write(17,0)
pi.stop()
print("bye")
