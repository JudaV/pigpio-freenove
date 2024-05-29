import pigpio
 
button_pin = 18         # set button_pin vatiable to GPIO18
led_pin = 17            # define led_pin to BCM GPIO17
pi1 = pigpio.pi()       # Initialise Pi connection and access to the local Pi's GPIO


def setup():
    print ('using pin %d and pin %d' % (led_pin, button_pin))


def loop():
    while True:
        if pi1.read(button_pin) == 0:
            pi1.write(led_pin, 1) 
        else:
            pi1.write(led_pin, 0)
        

def destroy():
    pi1.stop()                       # Release all GPIO
    print("program terminated")

if __name__ == '__main__':           # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\n program stopped by Keyboard Interrupt")
        
    finally:
        destroy()