#include <stdio.h>
#include <pigpio.h>

/*
gcc -pthread -o wave wave.c -lpigpio
*/

int gpios[] = {18,23,24,25};

// 

gpioPulse_t pulses[] =
{
   {(1<<18), (1<<25), 50000}, 
   {(1<<23), (1<<18), 50000}, 
   {(1<<24), (1<<23), 50000},
   {(1<<25), (1<<24), 50000}
};

// gpioPulse_t pulses[] =
// {
//    {0x40000, 0x3800000, 5000}, 
//    {0x800000, 0x3040000, 5000}, 
//    {0x1000000, 0x2840000, 5000}, 
//    {0x2000000, 0x1840000, 5000}, 
// };


int main(int argc, char *argv[])
{
   int g, wid=-1;

   if (gpioInitialise() < 0) return 1;

   for (g=0; g<sizeof(gpios)/sizeof(gpios[0]); g++){
      gpioSetMode(gpios[g], PI_OUTPUT);
      gpioWrite(gpios[g], 0);
   }

   gpioWaveClear();
   gpioWaveAddGeneric(4, pulses);
   wid = gpioWaveCreate();
   if (wid >= 0)
   {
      gpioWaveTxSend(wid, PI_WAVE_MODE_REPEAT);
      time_sleep(10);
      gpioWaveTxStop();
      gpioWaveDelete(wid);
   }
   gpioWrite(18,0);
   gpioWrite(23,0);
   gpioWrite(24,0);
   gpioWrite(25,0);
   gpioTerminate();
}

