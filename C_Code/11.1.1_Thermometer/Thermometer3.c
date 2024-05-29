#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <pigpio.h>
#include <ncurses.h> 
#include <math.h>

#define PCF8591_I2C_ADDR 0x48

int main(int argc, char *argv[])
{
    int i;
    int r;
   int handle;
   char aout;
   char command[2];
   // unsigned char value[4];
   unsigned char str[8];
   int value;

   int j;
   int key;

   if (gpioInitialise() < 0) return 1;

   initscr();
   noecho();
   cbreak();
   nodelay(stdscr, true);
   curs_set(0);

   printw("PCF8591  - press any key to quit.");

   mvaddstr(10, 0, "Thermometer");
   refresh();

   handle = i2cOpen(1, PCF8591_I2C_ADDR, 0);

   command[1] = 0;
   aout = 128;
   float voltage;

   while (1)
   {
        command[1] = aout;
        command[0] = 0x40 | (0x07); // output enable | read input i

        i2cWriteDevice(handle, &command, 2);
        value = i2cReadByte(handle);
        voltage = value / 255.0 * 3.3;
        float Rt = 10 * voltage / (3.3 - voltage); //calculate resistance value of thermistor
        float tempK = 1/(1/(273.15 + 25) + log(Rt/10)/3950.0); //calculate temperature (Kelvin)
        float tempC = tempK - 273.15; //calculate temperature (Celsius)

        sprintf(str, "%3d, %f, temp %.1fC", value, voltage, tempC);
    
        mvaddstr(10 , 18, str);
        refresh();
        gpioPWM(17, value); //  just one line to get the LED on
        key = getch();
        if (key != -1)
        break;
   }
   endwin();
   i2cClose(handle);
   gpioWrite(17,1);
   gpioTerminate();
   return (0);
}
