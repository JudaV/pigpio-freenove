#include <pigpio.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

#define ledPinRed    17
#define ledPinGreen  23
#define ledPinBlue   27


void setLedColor(int r, int g, int b)
{
	gpioPWM(ledPinRed,   r);	// Set the duty cycle for each color
	gpioPWM(ledPinGreen, g);
	gpioPWM(ledPinBlue,  b);
}

volatile int keepRunning = 1;
void intHandler(int dummy) {
    keepRunning = 0; 
}

int main(int argc, char *argv[]){   
    if (gpioInitialise() < 0){
        printf("Error: failed to initialize the GPIO interface\n");
        return 1;
    }
    else {
        printf("GPIO interface initialized\n");
		gpioSetPWMrange(ledPinRed, 2000);
		gpioSetPWMrange(ledPinGreen, 2000);
		gpioSetPWMrange(ledPinBlue, 2000);
		gpioSetPWMfrequency(ledPinRed, 5000);
		gpioSetPWMfrequency(ledPinGreen, 5000);
		gpioSetPWMfrequency(ledPinBlue, 5000);
    }

	int r,g,b;
	signal(SIGINT, intHandler);
	while(keepRunning){

		r=rand()%90;  //get a random in (0,90) (modulo 90)
		g=rand()%90;  // get a random in (0,90)
		b=rand()%90;  // get a random in (0,90)
		

		setLedColor(r,g,b);  // set random as the duty cycle value 
		printf("r=%d,  g=%d,  b=%d \n",r,g,b);
		gpioSleep(PI_TIME_RELATIVE, 2, 300000); // sleep for 1.30 seconds
		gpioWrite(ledPinRed, 1);
		gpioWrite(ledPinGreen, 1);
		gpioWrite(ledPinBlue,1);
		gpioSleep(PI_TIME_RELATIVE, 0, 50000);
	}

	gpioWrite(ledPinRed, 1);
	gpioWrite(ledPinGreen, 1);
	gpioWrite(ledPinBlue,1);
    gpioTerminate();
	printf("\nBye\n");
	return 0;
}
