/*
 * Filename:    LCD3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use of LCD 1602 display
 * Author:      JudaV
 * date:        october 2024
 * compile:     gcc -o LCD3 LCD3.c -lpigpio -lpthread
 *              or with makefile:  make
 * usage:       sudo ./LCD3
 */

/* File connecting LCD1602 to pi through i2c using the pigpio library
the connection of the pins as follows:

PCF8574T P7   P6   P5   P4   P3   P2   P1   P0
    MSB  |    |    |    |    |    |    |    |  Least Signifant Bit
HD44780  B7   B6   B5   B4   BL   E    RW   RS
         --- data-bits----   --- control-bits ---

Explanation:
E pin is the clock, information gets read bij the LCD on falling edge (E1 -> E0)
As can been seen from this diagram, data gets read B7 through B4. B3 through B0 are not
connected.
That's why it is called 4-bit. The control-bits BL E RW RS must always be set / send.
Each byte we send has 4 data bits and 4 control bits.

Sending 4-bit information gets done by sending the most signifant 4bit nibble first.
So sending information is as follows: 4bit MSB first with E bit high, 4bit MSB E-bit low
4bit LSB with E-bit high, 4 bit LSB with E-bit low.

Using the data sheet, we can fill in the control-bits
(e.g. : https://cdn-shop.adafruit.com/datasheets/TC1602A-01T.pdf) */

#include <stdio.h>
#include <pigpio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <signal.h>

#define LCD_ADRESS 0x27
int handle;
int keepRunning = 1;
void writeCommand(unsigned char byte);
void writeData(unsigned char byte);
void initialise_lcd(void);
void writeBufferContentToLCD(char *buf, int lenTxt, int line);

void printDataTime();
void writeCPUTempToLCD();

void intHandler(int dummy);

unsigned char *buffer = NULL;
unsigned char *buffer2 = NULL;

int main(int argc, char *argv[])
{
    if (gpioInitialise() < 0)
        return 1;
    handle = i2cOpen(1, LCD_ADRESS, 0);
    initialise_lcd();
    printf("control-C to terminate\n");

    signal(SIGINT, intHandler);
    // call the function that reads the cpu temp from file
    // and outputs it to the LCD
    writeCPUTempToLCD();
    while (keepRunning)
    {
        // call the function that reads the current time and puts it on the LCD
        printDataTime();
        gpioSleep(PI_TIME_RELATIVE, 1, 0); // wait one second
    }

    writeCommand(0x01); // clear leds
    gpioTerminate();
    return 0;
}

void writeCommand(unsigned char byte)
// send 4 bytes to transmit one byte..
{
    unsigned char bytesToSend[4];
    bytesToSend[0] = (byte & 0xF0) | 0x0C;        // 4bit MSB first with E bit high,
                                                  // BL   E    RW   RS
                                                  // 1    1    0    0  gives 0xC
    bytesToSend[1] = (byte & 0xF0) | 0x08;        // 4-bit MSB E-bit low gives 0x8:  1 1 0 0
    bytesToSend[2] = ((byte << 4) & 0xF0) | 0x0C; // 4-bit LSB with E-bit high,
    bytesToSend[3] = ((byte << 4) & 0xF0) | 0x08; // 4-bit LSB with E-bit low.
    gpioSleep(PI_TIME_RELATIVE, 0, 500);
    i2cWriteDevice(handle, bytesToSend, 4);
}

void writeData(unsigned char byte)
{
    unsigned char bytesToSend[4];
    bytesToSend[0] = (byte & 0xF0) | 0x0D;        // 4bit MSB first with E bit high,
                                                  // BL   E    RW   RS
                                                  // 1    1    0    1  gives 0xD
    bytesToSend[1] = (byte & 0xF0) | 0x09;        // 4bit MSB E-bit low gives 0x9 : 1 0 0 1
    bytesToSend[2] = ((byte << 4) & 0xF0) | 0x0D; // 4bit LSB with E-bit high,
    bytesToSend[3] = ((byte << 4) & 0xF0) | 0x09; // 4 bit LSB with E-bit low.
    gpioSleep(PI_TIME_RELATIVE, 0, 500);
    i2cWriteDevice(handle, bytesToSend, 4);
}

void initialise_lcd(void) // initialisation sequence:
{                         // the 1602A seems not to need the first 8 lines, uncomment for 1602
    // gpioSleep(PI_TIME_RELATIVE, 0, 150000);
    // writeCommand(0x30);
    // gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    // writeCommand(0x30);
    // gpioSleep(PI_TIME_RELATIVE, 0, 110000);
    // writeCommand(0x30);  // function set
    // gpioSleep(PI_TIME_RELATIVE, 0, 10000);
    writeCommand(0x20); // set to 4-bits
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x20);
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x28); // 4 bit , 2 lines, and 5x8bit fonts
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x0C); // cursor off
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x01); // clear screen
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
}

void writeBufferContentToLCD(char *buf, int lenTxt, int line)
// line is 1 for upper line, line=2 for lower line
{
    if (line != 2)
    {
        writeCommand(0x80); // writes to first line, first position of LCD
    }
    else if (line == 2)
    {
        writeCommand(0xC0); // writes lower line, first position of LCD
    }

    if (lenTxt > 16)
        lenTxt = 16;
    for (int i = 0; i < lenTxt; i++)
    {
        writeData(buf[i]);
    }
}

void printDataTime()
{
    // Display system time on LCD
    unsigned char *buffer2 = malloc(34 * sizeof(char));
    time_t rawtime;
    struct tm *timeinfo;
    int size2 = 0;
    time(&rawtime);                 // get system time
    timeinfo = localtime(&rawtime); // convert to local time
    // print time-info to buffer and determine size of the output
    size2 = snprintf(buffer2, 16, "Time:%02d:%02d:%02d", timeinfo->tm_hour, timeinfo->tm_min, timeinfo->tm_sec);
    writeBufferContentToLCD(buffer2, size2, 2);
    free(buffer2);
}

void writeCPUTempToLCD()
{
    unsigned char *buffer = malloc(34 * sizeof(char));

    FILE *fp;
    char str_temp[15];
    float CPU_temp;
    // CPU temperature data is stored in this directory as a written number e.g. '47760.
    fp = fopen("/sys/class/thermal/thermal_zone0/temp", "r");
    fgets(str_temp, 15, fp);            // read file temp
    CPU_temp = atof(str_temp) / 1000.0; // convert to Celsius degrees
    // determine size of string and display CPU temperature on LCD
    int size = snprintf(buffer, 16, "CPU:%.2fC", CPU_temp);
    fclose(fp);

    writeBufferContentToLCD(buffer, size, 1);
    free(buffer);
}

void intHandler(int dummy)
{
    keepRunning = 0;
}