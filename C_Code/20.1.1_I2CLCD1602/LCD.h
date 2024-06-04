/* File connecting LCD1602 to pi through i2c using the pigpio library 
the connection of the pins as follows

PCF8574T P7   P6   P5   P4   P3   P2   P1   P0  
    MSB  |    |    |    |    |    |    |    |  Least Signifant Bit
HD44780  B7   B6   B5   B4   BL   E    RW   RS
         --- data-bits----   --- control-bits ---

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



#include <pigpio.h>
int handle;
void writeCommand(char byte)
// send 4 bytes to transmit one byte..
{   
    char bytesToSend[4];
    bytesToSend[0] = (byte&0xF0)|0x0C ;       // 4bit MSB first with E bit high, 
                                              // BL   E    RW   RS 
                                              // 1    1    0    0  gives 0xC
    bytesToSend[1] = (byte&0xF0)|0x08;        // 4bit MSB E-bit low gives 0x8:  1 1 0 0 
    bytesToSend[2] = ((byte<<4)&0xF0)|0x0C ;  // 4bit LSB with E-bit high, 
    bytesToSend[3] = ((byte<<4)&0xF0)|0x08 ;  // 4 bit LSB with E-bit low.
    gpioSleep(PI_TIME_RELATIVE, 0, 500);
    i2cWriteDevice(handle, bytesToSend, 4);
}

void writeData(char byte)
{
    char bytesToSend[4];
    bytesToSend[0] = (byte&0xF0)|0x0D ;       // 4bit MSB first with E bit high, 
                                              // BL   E    RW   RS 
                                              // 1    1    1    0  gives 0xD
    bytesToSend[1] = (byte&0xF0)|0x09;        // 4bit MSB E-bit low gives 0x9
    bytesToSend[2] = ((byte<<4)&0xF0)|0x0D ;  // 4bit LSB with E-bit high, 
    bytesToSend[3] = ((byte<<4)&0xF0)|0x09 ;  // 4 bit LSB with E-bit low.
    gpioSleep(PI_TIME_RELATIVE, 0, 500);
    i2cWriteDevice(handle, bytesToSend, 4);
}

void initialise_lcd(void) // initialisation sequence:
{   // the 1602A seems not to need the first 8 lines, uncomment voor 1602
    // gpioSleep(PI_TIME_RELATIVE, 0, 150000);
    // writeCommand(0x30);
    // gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    // writeCommand(0x30);
    // gpioSleep(PI_TIME_RELATIVE, 0, 110000);
    // writeCommand(0x30);  // function set
    // gpioSleep(PI_TIME_RELATIVE, 0, 10000);
    writeCommand(0x20);  // set to 4-bits
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x20);
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x28);  // 4 bit , 2 lines, and 5x8bit fonts 
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x0C);   // cursor off
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
    writeCommand(0x01);  // clear screen
    gpioSleep(PI_TIME_RELATIVE, 0, 5000);
}

void writeBufferContentToLCD(char *buf, int lenTxt, int line)
// line is 1 for upper line, line=2 for lower line
{
    if (line!=2)
    {
        writeCommand(0x80); // writes to first line, first position of LCD
    }
    else if (line == 2)
    {
        writeCommand(0xC0);  // writes lower line, first position of LCD
    }

    if (lenTxt > 16) lenTxt = 16;
    for (int i = 0; i < lenTxt; i++)
        {
            writeData(buf[i]);
        }
}
