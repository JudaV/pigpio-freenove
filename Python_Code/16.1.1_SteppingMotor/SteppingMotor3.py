import pigpio
import time

pi = pigpio.pi()

G1 = 18     # set broadcom pin numbers
G2 = 23
G3 = 24
G4 = 25
pins = [G1, G2, G3, G4]

def setup():
    for pin in pins:
        pi.set_mode(pin, pigpio.OUTPUT)
        pi.write(pin,0)

def loop():
    flash_500=[] # flash every 500 ms
    flash_100=[] # flash every 100 ms
    delay_1 = 500000
    delay_2 = 6000

    #                              ON     OFF  DELAY
    flash_500.append(pigpio.pulse(1<<G1, 1<<G4, delay_1)) # the on and off positions are bitmasks
    flash_500.append(pigpio.pulse(1<<G2, 1<<G1, delay_1))
    flash_500.append(pigpio.pulse(1<<G3, 1<<G2, delay_1))
    flash_500.append(pigpio.pulse(1<<G4, 1<<G3, delay_1))


    flash_100.append(pigpio.pulse(1<<G1, 1<<G4, delay_2))
    flash_100.append(pigpio.pulse(1<<G2, 1<<G1, delay_2))
    flash_100.append(pigpio.pulse(1<<G3, 1<<G2, delay_2))
    flash_100.append(pigpio.pulse(1<<G4, 1<<G3, delay_2))

    pi.wave_clear() # clear any existing waveforms

    pi.wave_add_generic(flash_500) # 500 ms flashes
    f500 = pi.wave_create() # create and save id

    pi.wave_add_generic(flash_100) # 100 ms flashes
    f100 = pi.wave_create() # create and save id

    pi.wave_send_repeat(f500)
    print("f500")
    time.sleep(10)
    
    pi.wave_send_repeat(f100)
    print("f100")
    time.sleep(10)


def destroy():
    pi.wave_tx_stop() # stop waveform
    pi.wave_clear() # clear all waveform
    for pin in pins:
        pi.write(pin,0)
    pi.stop()                       # Release all GPIO
    print("program terminated")


if __name__ == '__main__':           # Program entrance
    print ('Program is starting ...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:        # Press ctrl-c to end the program.
        print("\nprogram stopped by Keyboard Interrupt")
        
    finally:
        destroy()
