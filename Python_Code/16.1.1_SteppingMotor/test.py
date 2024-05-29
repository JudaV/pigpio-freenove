import pigpio
import time

pi = pigpio.pi()


G1=4
G2=24

pi.set_mode(G1, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

flash_500=[] # flash every 500 ms
flash_100=[] # flash every 100 ms

#                              ON     OFF  DELAY

flash_500.append(pigpio.pulse(1<<G1, 1<<G2, 500000))
flash_500.append(pigpio.pulse(1<<G2, 1<<G1, 500000))

flash_100.append(pigpio.pulse(1<<G1, 1<<G2, 100000))
flash_100.append(pigpio.pulse(1<<G2, 1<<G1, 100000))

pi.wave_clear() # clear any existing waveforms

pi.wave_add_generic(flash_500) # 500 ms flashes
f500 = pi.wave_create() # create and save id

pi.wave_add_generic(flash_100) # 100 ms flashes
f100 = pi.wave_create() # create and save id

pi.wave_send_repeat(f500)

time.sleep(4)

pi.wave_send_repeat(f100)

time.sleep(4)

pi.wave_send_repeat(f500)

time.sleep(4)

pi.wave_tx_stop() # stop waveform

pi.wave_clear() # clear all waveforms