/*
 * Filename:    UltrasonicRanging3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: read from a HC SR04 ultrasonic ranging module
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o UltrasonicRanging3 UltrasonicRanging3.c -lpigpio -lpthread
 *              or with makefile:  make
 * usage:       sudo ./UltrasonicRanging3
 */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

int trigPin = 23; // define trigger pin and echo pin
int echoPin = 24;

uint32_t highTick = 0;
uint32_t lowTick = 0;
uint32_t pulseTime = 0;
double distance;

volatile int keepRunning = 1;
void intHandler(int dummy);
void setup(int trigPin, int echoPin);
void trigger();
void receiveCallBack(int gpio, int level, uint32_t tick);

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
    setup(trigPin, echoPin);
    signal(SIGINT, intHandler);

    while (keepRunning)
    {
        trigger();
        gpioSetAlertFunc(echoPin, receiveCallBack); // catch rising edge
        gpioSetAlertFunc(echoPin, receiveCallBack); // catch falling edge
        gpioSleep(PI_TIME_RELATIVE, 1, 0);
        highTick = 0; // to start measuring again
        lowTick = 0;
    }

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
void setup(int trigPin, int echoPin)
{
    gpioSetMode(trigPin, PI_OUTPUT);
    gpioSetMode(echoPin, PI_INPUT);
    gpioGlitchFilter(echoPin, 100);
}

void trigger()
{
    gpioWrite(trigPin, 0);
    gpioSleep(PI_TIME_RELATIVE, 1, 500); // wait 1,5s
    gpioWrite(trigPin, 1);
    gpioDelay(10); // send 10us pulse
    gpioWrite(trigPin, 0);
}

void receiveCallBack(int gpio, int level, uint32_t tick)
{
    if (level == 1) // rising edge
    {
        highTick = tick;
    }
    else
    {
        lowTick = tick; // level 0 means falling edge
    }
    if ((highTick > 0) && (lowTick > 0))
    {
        pulseTime = (lowTick - highTick); // lowTick is later, higher number
        if (pulseTime < 10000)            // filter missed ticks
        {
            printf("pulse_time: %d\n", pulseTime);
            distance = (float)((17 * pulseTime) / 1000.0);
            printf("The distance is:  %.2f cm\n", distance);
        }
    }
}