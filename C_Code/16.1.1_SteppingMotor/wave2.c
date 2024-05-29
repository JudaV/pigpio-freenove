#include <stdio.h>

#include <pigpio.h>

/*
gcc -pthread -o wave wave.c -lpigpio
*/

int gpios[] = {18,23,24,25,};

gpioPulse_t pulses[] =
{
   {0x40000, 0x3800000, 5000}, 
   {0x800000, 0x3040000, 5000}, 
   {0x1000000, 0x2840000, 5000}, 
   {0x2000000, 0x1840000, 5000}, 
};

int main(int argc, char *argv[])
{
   int g, wid=-1;

   if (gpioInitialise() < 0) return 1;

   for (g=0; g<sizeof(gpios)/sizeof(gpios[0]); g++)
      gpioSetMode(gpios[g], PI_OUTPUT);

   gpioWaveClear();
   gpioWaveAddGeneric(sizeof(pulses)/sizeof(pulses[0]), pulses);
   wid = gpioWaveCreate();
   if (wid >= 0)
   {
      gpioWaveTxSend(wid, PI_WAVE_MODE_REPEAT);
      time_sleep(10);
      gpioWaveTxStop();
      gpioWaveDelete(wid);
   }

   gpioTerminate();
}

