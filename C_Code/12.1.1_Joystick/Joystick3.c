#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <ncurses.h> /* libncurses5-dev */

/*
sudo apt-get install libncurses5-dev
gcc -o PCF8591 PCF8591.c -lcurses -lpigpio -lpthread
*/

#define PCF8591_I2C_ADDR 0x48

/*
    P4 The thermister voltage is provided at AIN 1.
    P5 The photocell voltage is provided at AIN 0.
    P6 The single turn 10K ohm trim pot voltage is provided at AIN 3.
*/

/*  
You control the device by sending it two bytes. 
The first is the command code. 
The second (here aout) is the byte to write to the digital to analogue converter.
The command byte is structured as follows.

7 6 5 4 3 2 1 0 
0 X X X 0 X X X
  | | |   | | |
  A B B   C D D

0 1 0 0 0 1 0 0 (0x40 => 0 1 0 0 0 0 0 0)

A 0 D/A inactive
  1 D/A active

B 00 four single ended inputs
  01 two differential inputs
  10 single ended and differential
  11 two differential inputs

C 0 no auto inc
  1 auto inc

D 00 select channel 0
  01 select channel 1
  10 select channel 2
  11 select channel 3

*/

int main(int argc, char *argv[])
{
    int i;
    int r;
    int handle;
    char aout;                    // analog output
    unsigned char command[2];      
    unsigned char value[4];
    unsigned char str[8];

    int j;
    int key;

    if (gpioInitialise() < 0) return 1;

    initscr();
    noecho();
    cbreak();
    nodelay(stdscr, true);
    curs_set(0);

    printw("PCF8591 + or - to change aout, any other key to quit.");

    mvaddstr(10, 0, "X - axis");
    mvaddstr(12, 0, "Y - axis");
    mvaddstr(14, 0, "Z - button");
    mvaddstr(16, 0, "");

    refresh();

    handle = i2cOpen(1, PCF8591_I2C_ADDR, 0);

    command[1] = 0;
    aout = 256;

    while (1)
    {
        for (i=0; i<4; i++)
        {
            command[1] = aout;
            command[0] = 0x40 | ((i + 1) & 0x03); // output enable | read input i

            // i2cWriteDevice(unsigned handle, char *buf, unsigned count)
            // handle: >=0, as returned by a call to i2cOpen
            // buf: an array containing the data bytes to write
            // count: >0, the number of bytes to write
            i2cWriteDevice(handle, &command, 2);

            usleep(20000);

            // the read is always one step behind the selected input
            // read = 1, write = i + 1
            value[i] = i2cReadByte(handle);
            aout  = 255;
            sprintf(str, "%3d", value[i]);
            if (i < 3){
                mvaddstr(10+i+i, 12, str);
                value[i] = value[i] / 4;
                move(10 + i + i, 16);
                
            
                for(j = 0; j < 64; j++)
                if(j < value[i]) addch('*'); else addch(' ');
            }
            
        }

        refresh();

        key = getch();

        if      ((key == '+') || (key == '=')) aout++;
        else if ((key == '-') || (key == '_')) aout--;
        else if  (key != -1)   {
            command[1] = 0;
            command[0] = 0x40;
            i2cWriteDevice(handle, &command, 2);
            break;
        }                
        
    }

    endwin();
    aout= 0;
    i2cClose(handle);

    gpioTerminate();

    return (0);
}
