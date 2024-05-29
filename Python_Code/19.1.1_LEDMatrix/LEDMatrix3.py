import pigpio
import time

pi = pigpio.pi()

data_pin = 17   # connected to DS (14 on the IC)  - Serial data Input
latch_pin = 27  # connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising, 
                #     it will update the parallel data output.
clock_pin = 22  # connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is 
                # rising, serial data input register will do a shift.
pins = [data_pin, latch_pin, clock_pin]

# these lists give leds on as 1-s but or columns  have the leds on when they 
# are zero. (Common anode LED) We will have to invert them 
# so 00011100 becomes 11100011
# this done by masking with 0xff
# inverted a is (~a & 0xFF) see line 91
pic = [0x1c,0x22,0x51,0x45,0x45,0x51,0x22,0x1c]  # data of smiling face
data = [     # data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # " "
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00, # "0"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00, # "1"
    0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00, # "2"
    0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00, # "3"
    0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00, # "4"
    0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00, # "5"
    0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00, # "6"
    0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00, # "7"
    0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00, # "8"
    0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00, # "9"   
    0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00, # "A"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00, # "B"
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00, # "C"
    0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00, # "D"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00, # "E"
    0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00, # "F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # " "
]


def setup():
    for pin in pins:
        pi.set_mode(pin, pigpio.OUTPUT)
    

def clear_leds():   
    """     end the program with leds off: if rows and columns equal there is no current through the leds.
    """   
    pi.write(latch_pin, 0)
    time.sleep(0.001) 
    shift_out(0x00)
    shift_out(0x00)
    pi.write(latch_pin, 1)


def shift_out(byte,order="lsbfirst"):  # default is lsbfirst
    if order == "msbfirst":
        for i in range(7,-1,-1):
            pi.write(clock_pin, 0)
            pi.write(data_pin, byte>>i & 1) # rightshift value and bitmask 1 gives the last bit
            pi.write(clock_pin, 1)
    else:   # default lsbfirst
        for i in range(0, 8):   
            pi.write(clock_pin, 0)
            pi.write(data_pin, byte>>i & 1) # rightshift value and bitmask 1 gives the last bit
            pi.write(clock_pin, 1)


def loop():
    
    while True:
        # first the rows, as they are connected to the last register and must be shifted in first.
        # common anode led matrix means rows pos en columns negative to light up. 
        for j in range(0,250):
            x = 0x80
            for i in range(0,8):
                pi.write(latch_pin, 0) 
                shift_out(x)                 # rows first: rows is 1 means lighting up
                shift_out((~pic[i] & 0xff), "msbfirst")  # columns, zero means lightning up, 
                                             # so we invert pic[i] - see above
                                             #  lsbfirst has the smiley upside down, also good 
                pi.write(latch_pin, 1)       # now output byte to the leds
                time.sleep(0.00001)
                x >>= 1                      # move column one step x = x>>1
        for k in range(0,len(data)-8): #len(data) total number of "0-F" columns 
            for j in range(0,9): # times of repeated displaying LEDMatrix in every frame, the bigger the "j", the longer the display time.
                x=0x80      # Set the column information to start from the first column
                for i in range(k,k+8):
                    pi.write(latch_pin, 0) 
                    shift_out(x)                 # rows first: rows is 1 means lighting up
                    shift_out((~data[i] & 0xff), "msbfirst")  # columns, zero means lightning up, 
                                                # so we invert pic[i] - see above
                                                #  lsbfirst has the smiley upside down, also good 
                    pi.write(latch_pin, 1)       # now output byte to the leds
                    time.sleep(0.0001)
                    x >>= 1                      # move column one step x = x>>1
        break       # remove for continuous


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
        print("keyboard interrupt")
    finally:
        destroy()  
