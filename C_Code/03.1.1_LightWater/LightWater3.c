#include <pigpio.h>
#include <stdio.h>
#include <signal.h>

#define ledCounts 10
int pins[ledCounts] = {17,18,27,22,23,24,25,2,3,8};

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
    
    int j;
    // set the pins in write-mode and turn them off
    for (j= 0 ; j < ledCounts; j++){
        gpioSetMode(pins[j], PI_OUTPUT);
        gpioWrite(pins[j], 1);
    }
    signal(SIGINT, intHandler);
    while(keepRunning){
        int i;
		for(i=0;i<ledCounts;i++){   // move led(on) from left to right
			gpioWrite(pins[i], 0);
			gpioSleep(PI_TIME_RELATIVE, 1, 100000); // sleep for 1.1 seconds
			gpioWrite(pins[i], 1);
		}
		for(i=ledCounts-1;i>-1;i--){   // move led(on) from right to left
			gpioWrite(pins[i], 0);
			gpioSleep(PI_TIME_RELATIVE, 1, 100000); // sleep for 0.1 seconds
			gpioWrite(pins[i], 1);
		}
    }
    gpioTerminate();
	printf("\nBye\n");
	return 0;
}
