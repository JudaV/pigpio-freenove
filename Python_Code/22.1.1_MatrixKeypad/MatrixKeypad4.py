import pigpio
import time
from pigpio import pi

# pi = pigpio.pi() # instantiate keypad pi instance from the pigpio.pi class

row_pins = [18, 23, 24, 25] # BCM numbering - anodes 
col_pins = [10, 22, 27, 17] # cathodes

keypad = [[1, 2, 3, 'A'], [4, 5, 6, 'B'], [7, 8, 9, 'C'], ['*', 0, '#', 'D']]

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


    def record_input(self):
        output = None
        # set colums one by one low, 
        # then measure rows
        # then set cols high again
        for column_index, column in enumerate(col_pins):
            pi.write(column, 0)   # one col is low now, and ready to be read
            time.sleep(0.05)
            # now check the rows one by one in this column:
            for keypad_row_index, keypad_row in enumerate(row_pins):
                if pi.read(keypad_row) == 0:
                    # read the keypad list to get the correct character
                    output = keypad[keypad_row_index][column_index]
                    # time.sleep(0.1)
            pi.write(column,1)
        return output

pi = pigpio.pi()
kp = MatrixKeypad(pi)

def loop():
    while True:
        b = kp.record_input()
        time.sleep(0.1)
        if not b is None:
            print(f'{b} was pressed ')
            time.sleep(0.1)


def destroy():
    print(f"\nbye\n")
    pi.stop()




if __name__ == "__main__":
    print ('Program is starting ... \n')
    kp.setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")
        
    finally:
        destroy()
