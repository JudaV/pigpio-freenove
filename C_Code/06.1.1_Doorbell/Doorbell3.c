#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

int Button = 18;
int Buzzer = 17;
int level = 1;
static volatile int keepRunning = 1;

void intHandler(int dummy) {
    keepRunning = 0; 
}

int main(int argc, char *argv[])
{
	if (gpioInitialise() < 0) return 1;
	printf("pigpio initialized\n");
	printf("Using GPIO-pins %d and %d \n", Buzzer, Button);	// Output information on terminal
	gpioSetPullUpDown(Button, PI_PUD_UP);   // Sets a pull-up
    gpioSetMode(Buzzer, PI_OUTPUT);        	// Set GPIO17 as output
    
	signal(SIGINT, intHandler);				// upon ^C the signal function is called to terminate the process;
											// intHandler will change the variable keepRunning form 1 to 0
											// now the infinite while loop will end, and main will stop gracefully
	
	while(keepRunning)
	{
        level = gpioRead(Button);
		if (level == 0)
		{
            gpioWrite(Buzzer, 1);              // Make Buzzer output HIGH level, turn on
        }
        else
		{
            gpioWrite(Buzzer, 0);              // Make GPIO output LOW level, turn Buzzer off
        }
	}
	
	gpioTerminate();
	printf("\nBye\n");
	return 0;
}