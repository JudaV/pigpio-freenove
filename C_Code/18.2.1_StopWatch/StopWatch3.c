#include <pigpio.h>
#include <stdio.h>
#include <signal.h>
#include <unistd.h>

#define dataPin  24  // connected to DS (14 on the IC)  - Serial data Input
#define latchPin 23  // connected to ST-CP (12 on the IC)  - Parallel update output: when its electrical level is rising, 
                     //  it will update the parallel data output.
#define clockPin 18  // connected to SH_CP (11 on the IC) - Serial shift clock: when its electrical level is 
                     // rising, serial data input register will do a shift.
const int digitPin[] = {17, 27, 22, 10};        // Define 7-segment display common pin
// character 0-9 code of common anode 7-segment display 
unsigned char num[]={0xc0,0xf9,0xa4,0xb0,0x99,0x92,0x82,0xf8,0x80,0x90};
int counter = 0;    //variable counter,the number will be displayed by 7-segment display
int MSBFIRST = 1;
int LSBFIRST = 2;

void selectDigit(int digit);
void shiftOut(int dPin,int cPin,int order,int val);
void clearLeds();
void timer(int sig);
void outData(int data);
void display(int dec);

int main(int argc, char *argv[])
{
    int i,j = 0;
    
    if (gpioInitialise() < 0)
    {
        printf("Error: failed to initialize the GPIO interface\n");
        return 1;
    }
    else 
    {
        printf("GPIO interface initialized\n");
    }
    gpioSetMode(dataPin, PI_OUTPUT);
    gpioSetMode(clockPin, PI_OUTPUT);
    gpioSetMode(latchPin, PI_OUTPUT);

    //set the pin connected to 7-segment display common end to output mode
    for (i = 0; i<4; i++){
        gpioSetMode(digitPin[i],PI_OUTPUT);
        gpioWrite(digitPin[i],1);
    } 

    signal(SIGALRM,timer);  //configure the timer
    alarm(1);               //set the time of timer to 1s
    while(1){
        display(counter);   //display the number counter
    }
    clearLeds();
    gpioTerminate();
	printf("\nBye\n");
	return 0;
}

void clearLeds()  // set the 8 leds to zero
{
    gpioWrite(latchPin, 0);
    for (int i = 0; i < 8; i++)
    {
        gpioWrite(clockPin, 0);
        gpioWrite(dataPin, 1);  // high level means leds are off!
        gpioSleep(PI_TIME_RELATIVE, 0, 100000);
        gpioWrite(clockPin, 1);
    }
    gpioWrite(latchPin, 1);
}

//Open one of the 7-segment display and close the remaining three, the parameter digit is optional for 1,2,4,8
void selectDigit(int digit){    
    gpioWrite(digitPin[0],((digit&0x08) == 0x08) ? 0 : 1);
    gpioWrite(digitPin[1],((digit&0x04) == 0x04) ? 0 : 1);
    gpioWrite(digitPin[2],((digit&0x02) == 0x02) ? 0 : 1);
    gpioWrite(digitPin[3],((digit&0x01) == 0x01) ? 0 : 1);
}

void shiftOut(int dPin,int cPin,int order,int val){   
	int i;  
    for(i = 0; i < 8; i++){
        gpioWrite(cPin,0);
        if(order == LSBFIRST){
            gpioWrite(dPin,((0x01&(val>>i)) == 0x01) ? 1 : 0);
            gpioSleep(PI_TIME_RELATIVE, 0, 10);
		}
        else {   // if(order == MSBFIRST){
            gpioWrite(dPin,((0x80&(val<<i)) == 0x80) ? 1 : 0);
            gpioSleep(PI_TIME_RELATIVE, 0, 10);
		}
        gpioWrite(cPin,1);
        gpioSleep(PI_TIME_RELATIVE, 0, 10);
	}
}

void outData(int data){      //function used to output data for 74HC595
    gpioWrite(latchPin, 0);
    shiftOut(dataPin,clockPin,MSBFIRST,data);
    gpioWrite(latchPin, 1);
}

void display(int dec){    //display function for 7-segment display
	int delays = 100;
	outData(0xff);	  
    selectDigit(0x01);      //select the first, and display the single digit
    outData(num[dec%10]);   
    gpioSleep(PI_TIME_RELATIVE, 0, delays);         //display duration
    
    outData(0xff);    
    selectDigit(0x02);      //select the second, and display the tens digit
    outData(num[dec%100/10]);
    gpioSleep(PI_TIME_RELATIVE, 0, delays);
    
    outData(0xff);    
    selectDigit(0x04);      //select the third, and display the hundreds digit
    outData(num[dec%1000/100]);
    gpioSleep(PI_TIME_RELATIVE, 0, delays);
    
    outData(0xff);    
    selectDigit(0x08);      //select the fourth, and display the thousands digit
    outData(num[dec%10000/1000]);
    gpioSleep(PI_TIME_RELATIVE, 0, delays);
}

void timer(int sig){        //Timer function
    if(sig == SIGALRM){     //If the signal is SIGALRM, the value of counter plus 1, and update the number displayed by 7-segment display
        counter ++;         
        alarm(1);           //set the next timer time
        printf("counter : %d \n",counter);
    }
}
