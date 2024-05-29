#include <stdio.h>
#include <signal.h>
#include <math.h>
#include <pigpio.h>

static volatile int keepRunning = 1;

void intHandler(int dummy) {
    keepRunning = 0; 
}

int Button = 18;
int Buzzer = 17;
int level = 1;

void alertor(int pin){
	int x;
	double sinVal, toneVal;
	for(x=0;x<360;x++){ // frequency of the alertor is consistent with the sine wave 
		sinVal = sin(x * (M_PI / 180));		//Calculate the sinus. M_PI is defines as pi in math.h
		toneVal = 2000 + (sinVal * 500);		//Add the resonant frequency and weighted sine value 
        gpioSetPWMfrequency(Buzzer,toneVal);
		gpioDelay(1000);                     // wait 100 microsec
    }
}

int main(int argc, char *argv[]){

	if (gpioInitialise() < 0) return 1;
	printf("pigpio initialized\n");
    printf("Using GPIO-pins %d and %d \n", Buzzer, Button);	// Output information on terminal
	gpioSetPullUpDown(Button, PI_PUD_UP);   // Sets a pull-up
    gpioSetMode(Buzzer, PI_OUTPUT);        	// Set GPIO17 as output
    
	signal(SIGINT, intHandler);				// upon ^C the signal function is called to terminate the process;
											// intHandler will change the variable keepRunning form 1 to 0
											// now the infinite while loop will end, and main will stop gracefully
	while(keepRunning){
        level = gpioRead(Button);
		if (level == 0){
            gpioPWM(Buzzer,128);			    //output corresponding PWM
            alertor(Buzzer);              // Make Buzzer output HIGH level, turn on
            printf("button pushed\n");
            }
        else{
            gpioWrite(Buzzer, 0);              // Make GPIO output LOW level, turn Buzzer off
        }
	}
	gpioTerminate();
	printf("\nBye\n");
	return 0;
}
