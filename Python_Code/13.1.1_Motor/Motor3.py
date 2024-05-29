import time
import curses
import pigpio


YL_40 = 0x48
aout = 128
pi = pigpio.pi() # Connect to local Pi
handle = pi.i2c_open(1, YL_40, 0)
stdscr = curses.initscr()

# define the pins connected to L293D 
motoRPin1 = 17
motoRPin2 = 27
enablePin = 22


# motor function: determine the direction and speed of the motor according to the input ADC value input
def motor(ADC):
    value = ADC - 128
    if (value > 0):  # make motor turn forward
        pi.write(motoRPin1, 1)  # motoRPin1 output HIHG level
        pi.write(motoRPin2, 0)   # motoRPin2 output LOW level
        # print ('Turn Forward...')
    elif (value < 0): # make motor turn backward
        pi.write(motoRPin1, 0)  
        pi.write(motoRPin2, 1) 
        # print ('Turn Backward...')
    else :
        pi.write(motoRPin1, 0)  
        pi.write(motoRPin2, 0) 
        # print ('Motor Stop...')
    pi.set_PWM_dutycycle(enablePin, abs(value))


def setup():    
    curses.noecho()
    curses.cbreak()
    stdscr.addstr(10, 0, "Motor speed")
    stdscr.nodelay(1)

    pi.set_PWM_frequency(enablePin,1000)
    pi.set_PWM_dutycycle(22, 0) 
    pi.set_mode(motoRPin1, pigpio.OUTPUT)
    pi.set_mode(motoRPin2, pigpio.OUTPUT)


def loop():
    while True:
        # AIN0 connected red adress 0x04 
        pi.i2c_write_byte_data(handle, 0x40, aout)
        v = pi.i2c_read_byte(handle)
        time.sleep(0.04)
        motor(v)
        time.sleep(0.01)
        stdscr.addstr(10, 12, str(abs(128 - v)) + ' ')
        stdscr.refresh()
        c = stdscr.getch()

        if c != curses.ERR:
            break


def destroy():
    print ('Program is stopping ... ')
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    motor(128)
    pi.set_PWM_dutycycle(22, 0) 
    time.sleep(0.05)
    pi.i2c_close(handle)
    pi.stop()
    print("bye")


if __name__ == '__main__': 
    print ('Program is starting ... ')
    setup()
    loop()
    aout = 0    # turn off LED connected to aout
    destroy()
