# Code for Freenove starter kits using pigpiod

The Starter kits sold by [Freenove](https://freenove.com) are a fun introduction to electronics and using the Raspberry Pi IO-pins.
One of their drawbacks is the use of of the deprecated wiringPi library, for which documentation is hard to find nowadays.
For learning programming in C their code is useless as they switch to C++ after a few chapters without warning or explanation.

I re-wrote their project code  using the [pigpiod](https://abyz.me.uk/rpi/pigpio/) library, for both the C code and the python code.
This repository also reflects my learning curve using this library. I tried to let clarity and simplicity override being smart and concise.
The first chapters in both C and Python are more or less 'hello-world-level'. Around chapter 20  a little more advanced programming techniques as bitwise operations, hexadecimal numbering are used.


All the electronic projects gave the desired output on my Raspberry Pi4 using Raspbian (Buster).
I expect them to work on all raspberry Pi 1-4 version but not on the  Raspberry Pi5
Use it at your risk of course. Suggestions, remarks, and improvements are welcome.
