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
    4bit LSB with E-bit high, 
    4 bit LSB with E-bit low. 

Using the data sheet, we can fill in the control-bits
(e.g. : https://cdn-shop.adafruit.com/datasheets/TC1602A-01T.pdf) """

import pigpio
import time

pi = pigpio.pi() # Connect to local Pi.
# set I2C-adress
ADRESS = 0x27
handle = pi.i2c_open(1, ADRESS, 0)

def command_to_lcd(byte_sequence):
    bytes_to_send = bytearray()
    bytes_to_send[0] = (byte_sequence&0xF0)|0x0C ;       # 4bit MSB first with E bit high, 
                                                         # BL   E    RW   RS 
                                                         # 1    1    0    0  gives 0xC
    bytes_to_send[1] = (byte_sequence&0xF0)|0x08;        # 4bit MSB E-bit low gives 0x8:  1 1 0 0 
    bytes_to_send[2] = ((byte_sequence<<4)&0xF0)|0x0C ;  # 4bit LSB with E-bit high, 
    bytes_to_send[3] = ((byte_sequence<<4)&0xF0)|0x08 ;  # 4bit LSB with E-bit low.
    time.sleep(0.0001)
    pi.i2c_write_device(handle, bytes_to_send)

def data_to_lcd(byte_sequence):
    bytes_to_send = bytearray()
    bytes_to_send[0] = (byte_sequence&0xF0)|0x0D ;       # 4bit MSB first with E bit high, 
                                                         # BL   E    RW   RS 
                                                         # 1    1    1    0  gives 0xD
    bytes_to_send[1] = (byte_sequence&0xF0)|0x09;        # 4bit MSB E-bit low gives 0x9
    bytes_to_send[2] = ((byte_sequence<<4)&0xF0)|0x0D ;  # 4bit LSB with E-bit high, 
    bytes_to_send[3] = ((byte_sequence<<4)&0xF0)|0x09 ;  # 4 bit LSB with E-bit low.
    time.sleep(0.0001)
    pi.i2c_write_device(handle, bytes_to_send)


def setup():
    ...
def loop():
    ...

def destroy():
    pi.i2c_close(handle)
    pi.stop()
    print("bye")

if __name__ == "__main__":  # Program entrance
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("keyboard interrupt")
    finally:
        destroy()