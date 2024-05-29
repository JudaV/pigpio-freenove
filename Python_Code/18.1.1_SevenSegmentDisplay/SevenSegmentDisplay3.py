import pigpio
import time

pi = pigpio.pi()

data_pin = 17   # connected to DS (14 on the IC)  - Serial data Input
latch_pin = 27  # connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising, 
                #     it will update the parallel data output.
clock_pin = 22  # connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is 
                # rising, serial data input register will do a shift.
pins = [data_pin, latch_pin, clock_pin]
num  = [0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90,0x88,0x83,0xc6,0xa1,0x86,0x8e, 0x7f,0x7f,0x7f]


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
        pi.write(data_pin,1)
        i += 1
        time.sleep(0.01)
        pi.write(clock_pin, 1)
    pi.write(latch_pin, 1)


def loop():
    # this will count the leds from 0 (leds out) tot 255 (all leds)
    while True:
        for x in num:
            pi.write(latch_pin, 0)
            for i in range(7,-1,-1):    # count back from 7 to 0 because:
                                        # Define segment “A” as the lowest level, the segment “DP” as the highest level, 
                                        # that is, from high to low: “DP”, “G”, “F”, “E”, “D”, “C”, “B”, “A”. 
                                        # And character "0" corresponds to the code: 1100 0000b=0xc0.
                bit  = x>>i & 1         # rightshift value and bitmask 1 gives the last bit
                pi.write(clock_pin, 0)
                pi.write(data_pin, bit)
                time.sleep(0.01)
                pi.write(clock_pin, 1)
            pi.write(latch_pin, 1) 
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
