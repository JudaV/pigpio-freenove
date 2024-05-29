#include <stdio.h>
#include <signal.h>
#include <pigpio.h>

static volatile int keepRunning = 1;
int gpioPin = 18;

void intHandler(int dummy) {
    keepRunning = 0; 
}

int main(int argc, char *argv[]){

	if (gpioInitialise() < 0) return 1;
	printf("pigpio initialized\n");
    gpioSetPWMfrequency(18, 50);  //the servo motor requires 50 Hz
    gpioSetPWMrange(18,1000); // set range 1000, so that zero degrees is 25 and 180 deg is 125 /1000
    printf("Using GPIO-pins %d \n", gpioPin);	
	
    
	signal(SIGINT, intHandler);				// upon ^C the signal function is called to terminate the process;
											// intHandler will change the variable keepRunning form 1 to 0
											// now the infinite while loop will end, and main will stop gracefully
	while(keepRunning){
        int i = 25;
        for (i = 25; i < 125; i++){
            gpioPWM(gpioPin, i);			         // output corresponding PWM
            gpioDelay(10000);                     // wait 10000 microsec, is 10ms
        }
        gpioDelay(50000);
        for (i = 124; i > 24; i--){
            gpioPWM(gpioPin, i);			         // output corresponding PWM
            gpioDelay(10000);                     // wait 10000 microsec, is 10ms
        }
        gpioDelay(50000);
        }
        
	gpioTerminate();
	printf("\nBye\n");
	return 0;
}
