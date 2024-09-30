/* gcc -o MatrixKeypad3 MatrixKeypad3.c -lpigpio -lpthread */

#include <pigpio.h>
#include <stdio.h>
#include <signal.h>
#define ROWS 4
#define COLS 4
int rowPins[4] = {18, 23, 24, 25}; // BCM numbering - anodes
int colPins[4] = {10, 22, 27, 17}; // cathodes

// key code
char keys[ROWS][COLS] = {
    {'1', '2', '3', 'A'},
    {'4', '5', '6', 'B'},
    {'7', '8', '9', 'C'},
    {'*', '0', '#', 'D'}};

void setup(int rowPins[], int colPins[]);

volatile int keepRunning = 1;
void intHandler(int dummy);

int main(int argc, char *argv[])
{
    char pressedkey = '0';
    if (gpioInitialise() < 0)
    {
        printf("Error: failed to initialize the GPIO interface\n");
        return 1;
    }
    else
    {
        printf("GPIO interface initialized\n");
    }
    setup(rowPins, colPins);
    signal(SIGINT, intHandler);
    int x, i, bit = 0;
    while (keepRunning)
    {

        // set colums one by one low,
        // then measure rows
        // then set cols high again
        for (int i = 0; i < COLS; ++i)
        {
            gpioWrite(colPins[i], 0); // one col is low now, and ready to be read
            gpioDelay(5000);          // ready to read during 0.05s
            // now check the **ROWS** one by one in this column:
            for (int j = 0; j < ROWS; ++j)
            {
                if (gpioRead(rowPins[j]) == 0)
                {
                    // read the keypad list to get the correct character
                    char pressedKey = keys[j][i];
                    printf("pressed: %c\n", pressedKey);
                    gpioSleep(PI_TIME_RELATIVE, 1, 500); // wait 0.1s
                }
            }
            gpioWrite(colPins[i], 1); // col could read, and back to silent
        }
    }
    gpioTerminate();
    printf("\nBye\n");
    return 0;
}

void intHandler(int dummy)
{
    keepRunning = 0;
}

// the board is setup as scanning the columns by sending low levels to the cols
// and measuring state in the rows when the col level is low.
void setup(int rowPins[], int colPins[])
{
    for (int i = 0; i < ROWS; i++)
    {
        gpioSetMode(rowPins[i], PI_INPUT);
        gpioSetPullUpDown(rowPins[i], PI_PUD_UP);
    }
    for (int j = 0; j < COLS; ++j)
    {
        gpioSetMode(colPins[j], PI_OUTPUT);
    }
}
