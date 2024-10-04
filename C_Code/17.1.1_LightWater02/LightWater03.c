/*
 * Filename:    LightWater03.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use of 74HC595 shift register and LED-bar
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o LightWater03 LightWater03.c -lpigpio -lpthread
 *              or with Makefile:  make
 * usage:       sudo ./LightWater03
 */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

#define dataPin 17  // connected to DS (14 on the IC)  - Serial data Input
#define latchPin 27 // connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising,
                    //  it will update the parallel data output.
#define clockPin 22 // connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is
                    // rising, serial data input register will do a shift.

volatile int keepRunning = 1;
void intHandler(int dummy);
void clearLeds();

int main(int argc, char *argv[])
{
    if (gpioInitialise() < 0)
    {
        printf("Error: failed to initialize the GPIO interface\n");
        return 1;
    }
    else
    {
        printf("GPIO interface initialized\n");
    }
    gpioSetMode(dataPin, PI_OUTPUT);
    gpioSetMode(clockPin, PI_OUTPUT);
    gpioSetMode(latchPin, PI_OUTPUT);

    signal(SIGINT, intHandler);
    int x, i, bit = 0;
    while (keepRunning)
    {
        for (x = 0; x < 256; x++)
        {
            printf("number:  %d\n", x);
            gpioWrite(latchPin, 0);
            for (i = 0; i < 8; i++)
            {

                gpioWrite(clockPin, 0);
                bit = x >> i & 1; // bitwise rightshift x and AND it with 1 to get last bit
                gpioSleep(PI_TIME_RELATIVE, 0, 20000);
                gpioWrite(dataPin, bit);
                gpioWrite(clockPin, 1);
            }
            gpioWrite(latchPin, 1);
        }
    }
    clearLeds();
    gpioTerminate();
    printf("\nBye\n");
    return 0;
}

void clearLeds() // set the 8 leds to zero
{
    gpioWrite(latchPin, 0);
    for (int i = 0; i < 8; i++)
    {
        gpioWrite(clockPin, 0);
        gpioWrite(dataPin, 0);
        gpioSleep(PI_TIME_RELATIVE, 0, 100000);
        gpioWrite(clockPin, 1);
    }
    gpioWrite(latchPin, 1);
}

void intHandler(int dummy)
{
    keepRunning = 0;
}