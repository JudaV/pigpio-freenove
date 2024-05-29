import pigpio
import time
import random

# pins = [17,23,27]         # define the pins for R:11,G:12,B:13 
pins = [22,27,17]
colors = ["r","g","b"]

pi1 = pigpio.pi()         # Initialise Pi connection and access to the local Pi's GPIO

def setup():
    for pin in pins:
        pi1.set_mode(pin, pigpio.OUTPUT)
        pi1.write(pin, 1)
          
    
def setColor(r,g,b):      # change duty cycle for three pins to r_val,g_val,b_val
    pi1.set_PWM_dutycycle(pins[0],255 - r) # at 0% PWM the light is ON!
    pi1.set_PWM_dutycycle(pins[1],255 - g) 
    pi1.set_PWM_dutycycle(pins[2],255 - b) 
    

def loop():
    while True : # LIGHT IS OFF AT 255!
        r = random.randint(0,255)  #get a random in (0,255)
        g = random.randint(0,255)
        b = random.randint(0,255)
        setColor(r,g,b)          #set random as a duty cycle value 
        print ('r=%d, g=%d, b=%d ' %(r ,g, b))
        time.sleep(1)
        
        
def destroy():
    for pin in pins:
        pi1.write(pin, 1)
    pi1.stop()                       # Release all GPIO
    print("\nprogram terminated\n")


if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
