"""  File connecting LCD1602 to pi through i2c using the pigpio library 
the connection of the pins as follows

PCF8574T P7   P6   P5   P4   P3   P2   P1   P0  
    MSB  |    |    |    |    |    |    |    |  Least Signifant Bit
HD44780  B7   B6   B5   B4   BL   E    RW   RS
         --- data-bits----   --- control-bits ---

E pin is the clock, information gets read bij the LCD on falling edge (E1 -> E0)
As can been seen from this diagram, data gets read B7 through B4. B3 through B0 are not
connected.
That's why it is called 4-bit. The control-bits BL E RW RS must always be set / send.
Each byte we send has 4 data bits and 4 control bits.

Sending 4-bit information gets done by sending the most signifant 4bit nibble first.
So sending information is as follows: 
    4bit MSB first with E bit high, (the e-bit works a bit like a clock-pin)
    4bit MSB E-bit low
    4bit LSB with E-bit high, (we get the LSB by left-shift 4 places)
    4 bit LSB with E-bit low. 

Using the data sheet, we can fill in the control-bits
(e.g. : https://cdn-shop.adafruit.com/datasheets/TC1602A-01T.pdf) """

import pigpio
import time
from datetime import datetime

pi = pigpio.pi() # Connect to local Pi.  (instantiate pigpio instance)
# set I2C-adress
ADRESS = 0x27
handle = pi.i2c_open(1, ADRESS, 0)


def command_to_lcd(bit_sequence):
    bytes_to_send = bytearray(4)
    bytes_to_send[0] = (bit_sequence&0xF0)|0x0C         # 4bit MSB first with E bit high, 
                                                         # BL   E    RW   RS 
                                                         # 1    1    0    0  gives 0xC
    bytes_to_send[1] = (bit_sequence&0xF0)|0x08         # 4bit MSB E-bit low gives 0x8:  1 1 0 0 
    bytes_to_send[2] = ((bit_sequence<<4)&0xF0)|0x0C    # 4bit LSB with E-bit high, 
    bytes_to_send[3] = ((bit_sequence<<4)&0xF0)|0x08    # 4bit LSB with E-bit low.
    time.sleep(0.0001)
    pi.i2c_write_device(handle, bytes_to_send)


def data_to_lcd(bit_sequence):
    bytes_to_send = bytearray(4)
    bytes_to_send[0] = (bit_sequence&0xF0)|0x0D         # 4bit MSB first with E bit high, 
                                                         # BL   E    RW   RS 
                                                         # 1    1    1    0  gives 0xD
    bytes_to_send[1] = (bit_sequence&0xF0)|0x09         # 4bit MSB E-bit low gives 0x9
    bytes_to_send[2] = ((bit_sequence<<4)&0xF0)|0x0D    # 4bit LSB with E-bit high, 
    bytes_to_send[3] = ((bit_sequence<<4)&0xF0)|0x09    # 4 bit LSB with E-bit low.
    time.sleep(0.0001)
    pi.i2c_write_device(handle, bytes_to_send)


def init():
    command_to_lcd(0x20)   # set to 4-bits
    time.sleep(0.005)
    command_to_lcd(0x20)
    time.sleep(0.005)
    command_to_lcd(0x28)   # 4 bit , 2 lines, and 5x8bit fonts 
    time.sleep(0.005)
    command_to_lcd(0x0C)   # cursor off
    time.sleep(0.005)
    command_to_lcd(0x01);  # clear screen
    time.sleep(0.005)


def string_to_lcd(string):
    for i in string:
        data_to_lcd(ord(i))
    time.sleep(0.005)


def write_strings_input():
    string1 = input("text for upper line: ")
    string2 = input("text for lower line: ")
    command_to_lcd(0x01)
    time.sleep(0.005)
    string_to_lcd(string1)
    command_to_lcd(0xC0)
    time.sleep(0.005)
    string_to_lcd(string2)


def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    string_to_lcd('{:.2f}'.format( float(cpu)/1000 ) + ' C')
 

def get_time_now():     # get system time
    string_to_lcd(datetime.now().strftime('    %H:%M:%S'))


def setup():
    init()


def loop():
    get_cpu_temp()
    command_to_lcd(0xC0) # start writing on the second line of the LCD
    get_time_now()
    write_strings_input()
    

def destroy():
    pi.i2c_close(handle)
    pi.stop()
    print("bye")


if __name__ == "__main__":
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("keyboard interrupt")
    finally:
        destroy()