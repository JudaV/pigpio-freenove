
#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

const int LED = 17;                       // define the ledPin
const int Button = 18;	                  // define the buttonPin

int ledState = 0;		                  // store the State of led
int buttonState = 1;	                  // store the State of button
int lastbuttonState = 1;                  // store the lastState of button
long lastChangeTime;	                  // store the change time of button state
long captureTime=50000;	                  // set the stable time as 50000 microsec ie 50ms
int reading;
volatile int keepRunning = 1;

void intHandler(int dummy) {
    keepRunning = 0; 
}

int main(int argc, char *argv[])
{
	if (gpioInitialise() < 0){
        printf("Error: failed to initialize the GPIO interface\n");
        return 1;
    }
    printf("GPIO interface initializedecho \nUsing GPIO-pins %d and %d \n", LED, Button);

	gpioSetMode(LED, PI_OUTPUT);          // Set ledPin to output
	gpioSetMode(Button, PI_INPUT);        // Set buttonPin to input
    gpioSetPullUpDown(Button, PI_PUD_UP); // pull up Button state to high level
	signal(SIGINT, intHandler);			  // upon ^C the signal function is called to terminate the process;
										  // intHandler will change the variable keepRunning form 1 to 0
										  // now the infinite while loop will end, and main will stop gracefully

	while(keepRunning){
		reading = gpioRead(Button);       // read the current state of button
		if( reading != lastbuttonState){  // if the button state has changed, record the time point
			lastChangeTime = gpioTick();
		}
		// if changing-state of the button last beyond the time we set, we consider that 
		// the current button state is an effective change rather than a bouncing
		if(gpioTick() - lastChangeTime > captureTime){
			// if button state is changed, update the data.
			if(reading != buttonState){
				buttonState = reading;
				//if the state is low, it means the action is pressing
				if(buttonState == 0){
					printf("Button is pressed\n");
					ledState = !ledState; //Reverse the LED state
					if(ledState){
						printf("turn on LED\n");
					}
					else {
						printf("turn off LED\n");
					}
				}
				//if the state is high, it means the action is releasing
				else {
					printf("Button is released\n");
				}
			}
		}
		gpioWrite(LED, ledState);
		lastbuttonState = reading;
	}
	gpioTerminate();
	printf("\nBye\n");
	return 0;
}
