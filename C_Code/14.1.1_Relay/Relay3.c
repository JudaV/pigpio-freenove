/*
 * Filename:    Relay3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use a relay module
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o Relay3 Relay3.c -lcurses -lpigpio -lpthread
 *              or with Makefile:  make
 * usage:       sudo ./Relay3
 */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>
// same code as Tablelamp
static volatile int keepRunning = 1;

void intHandler(int dummy)
{
    keepRunning = 0;
}

int main(int argc, char *argv[])
{
    int Button = 18;
    int Led = 17;
    int level = 1;

    if (gpioInitialise() < 0)
        return 1;
    printf("Using GPIO-pins %d and %d \n", Led, Button); // Output information on terminal
    gpioSetMode(Led, PI_OUTPUT);                         // Set GPIO17 as output
    signal(SIGINT, intHandler);                          // upon ^C the signal function is called to terminate the process;
                                                         // intHandler will change the variable keepRunning form 1 to 0
                                                         // now the infinite while loop will end, and main will stop gracefully
    while (keepRunning)
    {
        level = gpioRead(Button);
        if (level == 0)
        {
            gpioWrite(Led, 1); // Make LEd output HIGH level, turn on
        }
        else
        {
            gpioWrite(Led, 0); // Make GPIO output LOW level, turn Led off
        }
    }
    gpioTerminate();
    printf("\nBye\n");
    return 0;
}