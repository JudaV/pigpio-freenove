#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

#define ledPin 18

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
    }
	
	signal(SIGINT, intHandler);
	while(keepRunning){
		int i;
		for(i=0;i<256;i++){  //make the led brighter
			gpioPWM(ledPin, i); 
			gpioSleep(PI_TIME_RELATIVE, 0, 5000); // sleep for 0.05 seconds
		}
		for(i=255;i>=0;i--){  //make the led less bright
			gpioPWM(ledPin, i); 
			gpioSleep(PI_TIME_RELATIVE, 0, 5000); // sleep for 0.05 seconds
		}
	}

    gpioTerminate();
	printf("\nBye\n");
	return 0;
}
