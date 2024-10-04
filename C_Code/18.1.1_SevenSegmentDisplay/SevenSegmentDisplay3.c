/*
 * Filename:    SevenSegmentDisplay3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use of 74HC595 shift register for a 7-segment display
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o SevenSegmentDisplay3 SevenSegmentDisplay3.c -lpigpio -lpthread
 *              or with Makefile:  make
 * usage:       sudo ./SevenSegmentDisplay3
 */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

#define dataPin 17  // connected to DS (14 on the IC)  - Serial data Input
#define latchPin 27 // connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising,
                    //  it will update the parallel data output.
#define clockPin 22 // connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is
                    // rising, serial data input register will do a shift.

int num[] = {0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90, 0x88, 0x83, 0xc6, 0xa1, 0x86, 0x8e, 0x7f, 0x7f, 0x7f};
int hal_lo_Ien[] = {0x89, 0x88, 0xc7, 0xff, 0xc7, 0xc0, 0xff, 0xcf, 0x86, 0xab, 0x7f};
int hal_lo_Joost[] = {0x89, 0x88, 0xc7, 0xff, 0xc7, 0xc0, 0xff, 0xf1, 0xc0, 0xff, 0xc0, 0x92, 0xce, 0x7f};
int lenNum = sizeof(num) / sizeof(num[0]);

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
        for (x = 0; x < lenNum; x++)
        {
            gpioWrite(latchPin, 0);
            for (i = 7; i > -1; i--) // Count backwards because the order is DP-G-F-E-D-C-B-A
            {

                gpioWrite(clockPin, 0);
                bit = num[x] >> i & 1; // bitwise rightshift x and AND it with 1 to get last bit
                gpioSleep(PI_TIME_RELATIVE, 0, 50000);
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
        gpioWrite(dataPin, 1); // high level means leds are off!
        gpioSleep(PI_TIME_RELATIVE, 0, 100000);
        gpioWrite(clockPin, 1);
    }
    gpioWrite(latchPin, 1);
}

void intHandler(int dummy)
{
    keepRunning = 0;
}