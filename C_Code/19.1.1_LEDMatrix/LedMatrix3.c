/*
 * Filename:    LedMatrix3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use of 74HC595 shift register and LED matrix
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o LedMatrix3 LedMatrix3.c -lpigpio -lpthread
 *              or with makefile:  make
 * usage:       sudo ./LedMatrix3
 */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

#define dataPin 17  // connected to DS (14 on the IC)  - Serial data Input
#define latchPin 27 // connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising,
                    //  it will update the parallel data output.
#define clockPin 22 // connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is
                    // rising, serial data input register will do a shift.

int MSBFIRST = 1;
int LSBFIRST = 2;

volatile int keepRunning = 1;
void intHandler(int dummy);

void shiftOut(int Byte, int order);
void clearLeds();

// data of smiley face
unsigned char pic[] = {0x1c, 0x22, 0x51, 0x45, 0x45, 0x51, 0x22, 0x1c};
unsigned char data[] = {
    // data of "0-F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // " "
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x3E, 0x00, 0x00, // "0"
    0x00, 0x00, 0x21, 0x7F, 0x01, 0x00, 0x00, 0x00, // "1"
    0x00, 0x00, 0x23, 0x45, 0x49, 0x31, 0x00, 0x00, // "2"
    0x00, 0x00, 0x22, 0x49, 0x49, 0x36, 0x00, 0x00, // "3"
    0x00, 0x00, 0x0E, 0x32, 0x7F, 0x02, 0x00, 0x00, // "4"
    0x00, 0x00, 0x79, 0x49, 0x49, 0x46, 0x00, 0x00, // "5"
    0x00, 0x00, 0x3E, 0x49, 0x49, 0x26, 0x00, 0x00, // "6"
    0x00, 0x00, 0x60, 0x47, 0x48, 0x70, 0x00, 0x00, // "7"
    0x00, 0x00, 0x36, 0x49, 0x49, 0x36, 0x00, 0x00, // "8"
    0x00, 0x00, 0x32, 0x49, 0x49, 0x3E, 0x00, 0x00, // "9"
    0x00, 0x00, 0x3F, 0x44, 0x44, 0x3F, 0x00, 0x00, // "A"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x36, 0x00, 0x00, // "B"
    0x00, 0x00, 0x3E, 0x41, 0x41, 0x22, 0x00, 0x00, // "C"
    0x00, 0x00, 0x7F, 0x41, 0x41, 0x3E, 0x00, 0x00, // "D"
    0x00, 0x00, 0x7F, 0x49, 0x49, 0x41, 0x00, 0x00, // "E"
    0x00, 0x00, 0x7F, 0x48, 0x48, 0x40, 0x00, 0x00, // "F"
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // " "
};

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

    // signal(SIGINT, intHandler);

    // while(keepRunning)

    for (int j = 0; j < 200; j++)
    {
        int x = 0x80;
        for (int i = 0; i < 8; i++)
        {
            gpioWrite(latchPin, 0);
            shiftOut(x, MSBFIRST);                // rows first: rows is 1 means lighting up
            shiftOut((~pic[i] & 0xff), MSBFIRST); // columns 0 lights up, so we invert the bits this way
            gpioWrite(latchPin, 1);
            gpioSleep(PI_TIME_RELATIVE, 0, 500);
            x >>= 1; // shift column one row
        }
    }

    // show the contents
    for (int k = 0; k < sizeof(data) - 8; k++) // sizeof(data) total number of "0-F" columns
    {
        for (int l = 0; l < 20; l++)
        {
            int x = 0x80;
            int i = 0;
            for (i = k; i < 8 + k; i++)
            {
                gpioWrite(latchPin, 0);
                shiftOut(x, LSBFIRST);                 // rows first: rows is 1 means lighting up
                shiftOut((~data[i] & 0xff), MSBFIRST); // columns 0 lights up, so we invert the bits this way
                gpioWrite(latchPin, 1);
                gpioSleep(PI_TIME_RELATIVE, 0, 500);
                x >>= 1; // shift column one row
            }
        }
    }

    clearLeds();
    gpioTerminate();
    printf("\nBye\n");
    return 0;
}

void shiftOut(int Byte, int order)
{
    int i = 1;
    if (order == MSBFIRST)
    {
        for (i = 7; i >= 0; i--) // Count backwards means: Most Significant Bit First
        {
            gpioWrite(clockPin, 0);
            gpioSleep(PI_TIME_RELATIVE, 0, 50);
            gpioWrite(dataPin, Byte >> i & 1); // bitwise rightshift x and AND it with 1 to get last bit
            gpioWrite(clockPin, 1);
        }
    }
    else
    {
        int i = 0;
        for (i = 0; i < 8; i++) // LSBFIRST
        {
            gpioWrite(clockPin, 0);
            gpioSleep(PI_TIME_RELATIVE, 0, 50);
            gpioWrite(dataPin, Byte >> i & 1); // bitwise rightshift x and AND it with 1 to get last bit
            gpioWrite(clockPin, 1);
        }
    }
}

void clearLeds() // set the leds to zero:
                 // if rows and columns are both low, no current can flow so leds are off
{
    gpioWrite(latchPin, 0);
    shiftOut(0x00, MSBFIRST);
    shiftOut(0x00, MSBFIRST);
    gpioWrite(latchPin, 1);
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
}

void intHandler(int dummy)
{
    keepRunning = 0;
}