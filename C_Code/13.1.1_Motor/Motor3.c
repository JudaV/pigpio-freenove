/*
 * Filename:    Motor3.c
 * Project:     Freenove kit using pigpio C and Python library
 * Description: use of PCF8591 ADC chip to control the speed and direction of a DC motor
 * Author:      JudaV
 * date:        october 2024
 * compile:     sudo apt-get install libncurses5-dev
 *              gcc -o Motor3 Motor3.c -lcurses -lpigpio -lpthread
 *              or with Makefile:  make
 * usage:       sudo ./Motor3
 */

#include <stdio.h>
#include <pigpio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <ncurses.h>
#include <stdlib.h>

#define motorPin1 17 // define the pin connected to L293D
#define motorPin2 27
#define enablePin 22
#define PCF8591_I2C_ADDR 0x48

// motor function: determine the direction and speed of the motor according to the ADC
void motor(int ADC)
{
    int value = ADC - 128;
    if (value > 0)
    {
        gpioWrite(motorPin1, 1);
        gpioWrite(motorPin2, 0);
    }
    else if (value < 0)
    {
        gpioWrite(motorPin1, 0);
        gpioWrite(motorPin2, 1);
    }
    else
    {
        gpioWrite(motorPin1, 0);
        gpioWrite(motorPin2, 0);
    }
    gpioPWM(enablePin, abs(value));
}

int main(int argc, char *argv[])
{
    int r;
    int handle;
    char aout; // analog output
    unsigned char command[2];
    unsigned char value[4];
    unsigned char str[12];
    int j;
    int key;

    if (gpioInitialise() < 0)
        return 1;
    gpioSetPWMfrequency(enablePin, 1000);
    initscr();
    noecho();
    cbreak();
    nodelay(stdscr, true);
    curs_set(0);
    printw("PCF8591 + or - to change aout, any other key to quit.");

    mvaddstr(10, 0, "Motor speed");
    refresh();

    handle = i2cOpen(1, PCF8591_I2C_ADDR, 0);
    command[1] = 0;
    aout = 128; // analog output half-way
    int v;

    while (1)
    {
        command[1] = aout;
        command[0] = 0x40;
        // i2cWriteDevice(unsigned handle, char *buf, unsigned count)
        // handle: >=0, as returned by a call to i2cOpen
        // buf: an array containing the data bytes to write
        // count: >0, the number of bytes to write
        i2cWriteDevice(handle, command, 2);
        usleep(20000);
        // the read is always one step behind the selected input
        // read = 1, write = i + 1
        value[0] = i2cReadByte(handle);
        aout = 255;
        sprintf(str, "%3d", value[0]);
        v = value[0];
        motor(v);
        mvaddstr(10, 12, str);
        value[0] = value[0] / 4;

        for (j = 0; j < 64; j++)
            if (j < value[0])
                addch('*');
            else
                addch(' ');
        refresh();
        key = getch();
        if ((key == '+') || (key == '='))
            aout = 255;
        else if ((key == '-') || (key == '_'))
            aout = 0;
        else if (key != -1)
        {
            command[1] = 0;
            command[0] = 0x40;
            break;
        }
    }
    endwin();
    aout = 0;
    i2cClose(handle);
    gpioTerminate();
    return (0);
}
