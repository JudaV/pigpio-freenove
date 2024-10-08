# Filename: Calculator.py
# Project: Freenove kit using pigpio C and Python library
# Description: create a calculator using a matrix keypad and 1602 LCD display
# Author: JudaV
# date: october 2024


# This code uses the the LCD 1602A LCD and the 4x4 matrix keypad.
# The matrix keypad is connected in the same way as in the other files
# in this directory

# The LCD keypad is connected to 5V, ground SDA2 and  SCL just as in
# chapter 20.

# inputs from the matrix keypad are processed to the LCD1602A

import pigpio
import time
from pigpio import pi

# pins connected for keypad
row_pins = [18, 23, 24, 25]  # BCM numbering - anodes
col_pins = [10, 22, 27, 17]  # cathodes

# This is how it looks:
# keypad = [['1', '2', '3', 'A'], ['4', '5', '6', 'B'], ['7', '8', '9', 'C'], ['*', '0', '#', 'D']]

# This how we use it now:
# A becomes plus; B becomes minus; C becomes clear; D becomes division;  TODO #
keypad = [
    ["1", "2", "3", "+"],
    ["4", "5", "6", "-"],
    ["7", "8", "9", "C"],
    ["*", "0", ".", "/"],
]


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
        time.sleep(0.001)
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
            time.sleep(0.005)
        else:
            self.command_to_lcd(0xC0)  # start at second line
            time.sleep(0.005)
            self.string_to_lcd(string)  # write string to second line
            time.sleep(0.005)

    def clear(self):
        self.command_to_lcd(0x01)


class MatrixKeypad(pi):
    def __init__(self, pi):
        self.pi = pi

    def setup(self):
        # the board is setup as scanning the columns by sending low levels to the cols
        # and measuring state in the rows when the col level is low.
        for pin in row_pins:
            pi.set_mode(pin, pigpio.INPUT)
            pi.set_pull_up_down(pin, pigpio.PUD_UP)

        for pin in col_pins:
            pi.set_mode(pin, pigpio.OUTPUT)

    def record_char(self):
        output = None
        # set colums one by one low,
        # then measure rows
        # then set cols high again
        for column_index, column in enumerate(col_pins):
            pi.write(column, 0)  # one col is low now, and ready to be read
            time.sleep(0.005)
            # now check the rows one by one in this column:
            for keypad_row_index, keypad_row in enumerate(row_pins):
                if pi.read(keypad_row) == 0:
                    # read the keypad list to get the correct character
                    output = keypad[keypad_row_index][column_index]
                    time.sleep(0.05)
            pi.write(column, 1)
        return output


# connect to raspberry pi IO pins:
pi = pigpio.pi()

# set I2C-adress for LCD and connect
pi = pigpio.pi()
ADRESS = 0x27
handle = pi.i2c_open(1, ADRESS, 0)

# initialize screen and matrix keyboard:
lcd = LCD(pi)
kp = MatrixKeypad(pi)


def loop():
    temp_sum = 0
    num1 = 0
    num2 = 0
    operator = ""
    list_of_chars = []
    while True:
        b = kp.record_char()
        time.sleep(0.1)
        if b:  # if b is not None:
            print(f"{b} pressed")
            time.sleep(0.02)
            num1, num2, operator, list_of_chars = char_to_math_variables(
                b, list_of_chars, num1, num2, operator
            )
            if operator == "":
                lcd.write(1, align_right(f"{str(num1)}"))
            elif b in "+-/*":
                num1 = temp_sum
                lcd.write(1, align_right(f"{str(num1)} {operator}"))
            else:
                lcd.write(1, align_right(f"{str(num1)} {operator} {str(num2)}"))
            temp_sum = check_floats(calc(num1, operator, num2))
            lcd.write(2, align_right(str(temp_sum)))


def char_to_math_variables(b, list_of_chars, num1, num2, operator):
    if b in "01234567890.":
        list_of_chars.append(b)
        if list_of_chars:
            if operator:
                if "." in list_of_chars:
                    num2 = float("".join([str(item) for item in list_of_chars]))
                else:
                    num2 = int("".join([str(item) for item in list_of_chars]))
            else:
                if "." in list_of_chars:
                    num1 = float("".join([str(item) for item in list_of_chars]))
                else:
                    num1 = int("".join([str(item) for item in list_of_chars]))
    else:
        operator = b
        list_of_chars = []  # empty content for fresh new number
        if b == "/" or b == "*":
            num2 = 1  # prevent zerodiv error when evaluating before num2 is entered
        else:
            num2 = 0  # make room for new calculation
    return num1, num2, operator, list_of_chars


def calc(num1, operator, num2):
    num1 = check_floats(num1)
    num2 = check_floats(num2)
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "/":
        try:
            # if (float(int(num1) / int(num2))).is_integer():
            #     return int(int(num1) / int(num2))
            # else:
            #     return float(int(num1) / int(num2))
            return num1 / num2
        except ZeroDivisionError:
            lcd.write(2, "Zero Division Error")
            time.sleep(2)
            clear()
    elif operator == "*":
        return num1 * num2
    elif operator == "C":
        clear()
    else:  # when operator is ''
        return num1


def check_floats(s):
    if float(s).is_integer():
        return int(s)
    else:
        return float(s)


# I tried aligning to the right by sending the 0x1C command to the LCD but this
# returned unexpected results when using 2 lines. Same for 0x05
# this function proved far easier...
def align_right(string):
    length = len(string)
    return ((16 - length) * " ") + string


def clear():
    lcd.clear()


def destroy():
    pi.i2c_close(handle)
    pi.stop()
    print(f"\nbye\n")


if __name__ == "__main__":
    print("Program is starting ... \n")
    kp.setup()
    lcd.command_to_lcd(0x00)
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")

    finally:
        destroy()
