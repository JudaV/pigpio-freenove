import pigpio
import time

pi = pigpio.pi()

data_pin = 17   # connected to DS (14 on the IC)  - Serial data Input
latch_pin = 27  # connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising, 
                #     it will update the parallel data output.
clock_pin = 22  # connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is 
                # rising, serial data input register will do a shift.

pins = [data_pin, latch_pin, clock_pin]

def setup():
    for pin in pins:
        pi.set_mode(pin, pigpio.OUTPUT)
    

def clear_leds():   
    """     send 8 zero 's
    """   
    pi.write(latch_pin, 0)
    i = 0
    while i < 8:
        pi.write(clock_pin, 0)
        pi.write(data_pin,0)
        i += 1
        time.sleep(0.01)
        pi.write(clock_pin, 1)
    pi.write(latch_pin, 1)


def loop():
    # this will count the leds from 0 (leds out) tot 255 (all leds)
    while True:
        for x in range(0,255):
            pi.write(latch_pin, 0)
            for i in range(0,8):
                bit  = x>>i & 1  # rightshift value and bitmask 1 gives the last bit
                pi.write(clock_pin, 0)
                pi.write(data_pin, bit)
                time.sleep(0.01)
                pi.write(clock_pin, 1)
            pi.write(latch_pin, 1) 
            print(x)
            time.sleep(0.5)
        

def destroy():
    clear_leds()
    pi.stop()
    print("\nprogram terminated\n")

if __name__ == '__main__': # Program entrance
    print ('Program is starting...' )
    setup() 
    try:
        loop()  
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()  
