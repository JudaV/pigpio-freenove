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

Sending 4-bit information gets done by sending the Most Signifant Bit - 4bit nibble first.
So sending information is as follows: 
    4bit MSB first with E bit high,
    4bit MSB E-bit low
    4bit LSB with E-bit high, (we get the LSB by left-shift 4 places)
    4 bit LSB with E-bit low. 

Using the data sheet, we can fill in the control-bits
(e.g. : https://cdn-shop.adafruit.com/datasheets/TC1602A-01T.pdf) """

import pigpio
import time
from datetime import datetime
from pigpio import pi


class LCD(pi):
    def __init__(self, pi) -> None:
        self.pi = pi
        self.command_to_lcd(0x20)  # set to 4-bits
        time.sleep(0.005)
        self.command_to_lcd(0x20)
        time.sleep(0.005)
        self.command_to_lcd(0x28)  # 4 bit , 2 lines, and 5x8bit fonts
        time.sleep(0.005)
        self.command_to_lcd(0x0C)  # cursor off
        time.sleep(0.005)
        self.command_to_lcd(0x01)
        # clear screen
        time.sleep(0.005)

    def command_to_lcd(self, bit_sequence):
        bytes_to_send = bytearray(4)
        # 4bit MSB first with E bit high,
        # BL   E    RW   RS
        # 1    1    0    0  gives 0xC
        bytes_to_send[0] = (bit_sequence & 0xF0) | 0x0C

        # 4bit MSB E-bit low gives 0x8:  1 0 0 0
        bytes_to_send[1] = (bit_sequence & 0xF0) | 0x08
        # 4bit LSB with E-bit high: 1 1 0 0
        bytes_to_send[2] = ((bit_sequence << 4) & 0xF0) | 0x0C
        # 4bit LSB with E-bit low:  1 0 0 0
        bytes_to_send[3] = ((bit_sequence << 4) & 0xF0) | 0x08
        time.sleep(0.0001)
        self.pi.i2c_write_device(handle, bytes_to_send)

    def data_to_lcd(self, bit_sequence):
        bytes_to_send = bytearray(4)
        # 4bit MSB first with E bit high,
        # BL   E    RW   RS
        # 1    1    0    1    gives 0xD
        bytes_to_send[0] = (bit_sequence & 0xF0) | 0x0D
        # 4bit MSB E-bit low gives 0x9: 1 0 0 1
        bytes_to_send[1] = (bit_sequence & 0xF0) | 0x09
        # 4bit LSB with E-bit high,
        bytes_to_send[2] = ((bit_sequence << 4) & 0xF0) | 0x0D
        # 4 bit LSB with E-bit low.
        bytes_to_send[3] = ((bit_sequence << 4) & 0xF0) | 0x09
        time.sleep(0.0001)
        self.pi.i2c_write_device(handle, bytes_to_send)

    def string_to_lcd(self, string):
        for i in string:
            self.data_to_lcd(ord(i))
        time.sleep(0.005)

    def write_strings_input(self):
        string1 = input("text for upper line: ")
        string2 = input("text for lower line: ")
        self.command_to_lcd(0x01)  # clear
        time.sleep(0.005)
        self.string_to_lcd(string1)
        self.command_to_lcd(0xC0)  # second line
        time.sleep(0.005)
        self.string_to_lcd(string2)

    def write(self, line, string):
        """
        line = 1 for upper line
        line = 2 for lower lin3
        """
        if line != 2:
            self.command_to_lcd(0x01)  # clear
            time.sleep(0.005)
            self.string_to_lcd(string)  # write string to first line
        else:
            self.command_to_lcd(0xC0)  # start at second line
            time.sleep(0.005)
            self.string_to_lcd(string)  # write string to second line

    def clear(self):
        self.command_to_lcd(0x01)


pi1 = pigpio.pi()  # Connect to local Pi.  (instantiate pigpio instance)
# set I2C-adress
ADRESS = 0x27
handle = pi1.i2c_open(1, ADRESS, 0)
lcd = LCD(pi1)


def get_cpu_temp():  # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
    with open("/sys/class/thermal/thermal_zone0/temp") as file:
        cpu = file.read()
    return f"temp {float(cpu)/1000:.2f}C"


def get_time_now():  # get system time
    return datetime.now().strftime("    %H:%M:%S")


def loop():
    lcd.write(1, (get_cpu_temp()))  # write CPU temp to first line of lcd
    lcd.write(2, (get_time_now()))

    lcd.write_strings_input()
    time.sleep(5)
    lcd.write(1, "first line")
    lcd.write(2, "     second line")


def destroy():
    pi1.i2c_close(handle)
    pi1.stop()
    print("bye")


if __name__ == "__main__":
    print("Program is starting...")

    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("keyboard interrupt")
    finally:
        destroy()
