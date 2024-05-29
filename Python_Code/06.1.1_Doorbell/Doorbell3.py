import pigpio
 
button_pin = 18         # set button_pin variable to GPIO18
buzz_pin = 17           # define buzz_pin to BCM GPIO17
pi1 = pigpio.pi()       # Initialise Pi connection and access to the local Pi's GPIO

def setup():
    pi1.set_pull_up_down(button_pin, pigpio.PUD_UP)
    print ('using pin %d and pin %d' % (buzz_pin, button_pin))

def loop():
    while True:
        if pi1.read(button_pin) == 0:
            pi1.write(buzz_pin, 1) 
        else:
            pi1.write(buzz_pin, 0)

def destroy():
    pi1.stop()                       # Release all GPIO
    print("program terminated")


if __name__ == '__main__':           # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")
        
    finally:
        destroy()
