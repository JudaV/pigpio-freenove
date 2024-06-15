import pigpio
import time

pi = pigpio.pi() # instantiate keypad pi instance from the pigpio.pi class

row_pins = [18, 23, 24, 25] # BCM numbering - anodes 
col_pins = [10, 22, 27, 17] # cathodes

keypad = [[1, 2, 3, 'A'], [4, 5, 6, 'B'], [7, 8, 9, 'C'], ['*', 0, '#', 'D']]


def setup():
    # the board is setup as scanning the columns by sending low levels to the cols
    # and measuring state in the rows when the col level is low.
    for pin in row_pins:
        pi.set_mode(pin, pigpio.INPUT) 
        pi.set_pull_up_down(pin, pigpio.PUD_UP)
        
    for pin in col_pins:
        pi.set_mode(pin, pigpio.OUTPUT)

def record_keyboard_input():
    output = None
    for column in col_pins:
        pi.write(column,1)
    for col_index, col in enumerate(col_pins):
        pi.write(column,0)   # one col is low now, and ready to be read
        time.sleep(0.05)
        # now check the rows one by one in this column:
        for keypad_row_index, keypad_row in enumerate(row_pins):
            if pi.read(keypad_row) == 0:
                time.sleep(0.2)
                output = keypad[keypad_row_index][col_index]
                print(f' you pressed {output}')
        pi.write(col,1)
    if output:
        return output


def loop():
    # set colums one by one low, 
    # then measure rows
    # then set cols high again
    while True:
        record_keyboard_input()


def destroy():
    print(f"\nbye\n")
    pi.stop()


if __name__ == "__main__":
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")
        
    finally:
        destroy()
