
#include <pigpio.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>

static volatile int keepRunning = 1;

void intHandler(int dummy) {
    keepRunning = 0; 
}


int main(int argc, char *argv[])
{
   int GPIO=17;
   int level;

   if (gpioInitialise() < 0) return 1;

   //level = gpioRead(GPIO);
	
	gpioSetMode(GPIO, PI_OUTPUT);       // Set GPIO17 as output
	printf("Using GPIO-pin %d\n",GPIO);	// Output information on terminal
	signal(SIGINT, intHandler);			// upon ^C the signal function is called to terminate the process;
										// intHandler will change the variable keepRunning form 1 to 0
										// now the infinite while loop will end, and main will stop gracefully
	while(keepRunning){
		gpioSetMode(GPIO, PI_OUTPUT);   // Set GPIO17 as output
		gpioWrite(GPIO,1);              // Make GPIO output HIGH level
		printf("led turned on\n");		// Output information on terminal
		sleep(1);						// Wait for 1 second
		gpioWrite(GPIO,0);              // Make GPIO output LOW level
		printf("led turned off\n");		// Output information on terminal
		sleep(5);						// Wait for 5 seconds
	}
	gpioTerminate();
	printf("\nBye\n");
	return 0;
}

