/* gcc -o SenseLed3 SenseLed3.c -lpigpio -lpthread */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>
int ledPin = 18;    // define the ledPin
int sensorPin = 17; // define the sensorPin

volatile int keepRunning = 1;
void intHandler(int dummy);
void setup(int ledPin, int sensorPin);

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
    setup(ledPin, sensorPin);
    signal(SIGINT, intHandler);

    while (keepRunning)
    {
        gpioWrite(ledPin, 0);
        if (gpioRead(sensorPin))
        {
            gpioWrite(ledPin, 1);
            // printf("led turned on >>> \n");
        }
        else
        {
            gpioWrite(ledPin, 0);
            // printf("led turned off >>> \n");
        }
    }
    gpioWrite(ledPin, 0);
    gpioTerminate();
    printf("\nBye\n");
    return 0;
}

void intHandler(int dummy)
{
    keepRunning = 0;
}

/* The sensor will output high on sensing and low if not.
   So the sensorPin, needs to be pull down (set to) on not
   sensing. */
void setup(int ledPin, int sensorPin)
{
    gpioSetMode(sensorPin, PI_INPUT);
    gpioSetPullUpDown(sensorPin, PI_PUD_DOWN);
    gpioSetMode(ledPin, PI_OUTPUT);
}
