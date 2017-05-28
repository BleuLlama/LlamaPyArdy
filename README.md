# LlamaPyArdy
Somewhere between Firmata and a Bus Pirate... you'll find LlamaPyArdy...

LlamaPyArdy is a combination of a small Arduino script that takes commands over serial to do stuff, as well as a
python library on the desktop that talks with it.

The system currently supports:

Arduino script:
 - Serial interface running at 115200 baud
 - All commands are ascii printable, pseudo-human readable/writable
 - All commands return a 16 bit value
 - Support for hardware:
   - General Port IO for analog and digital reading and writing on all port pins
   - LED blinker routines for standard D13 LED, or another port pin it might be on
   - EEPROM storage/saving via "config" routines
   - I2C read/write of 8/16 bit values
   - I2C read/write of 8 bit value with no register defined
   - Adafruit WS2801 LED strand support (define the pins in the code)

Python script:
 - Autoscanning and connecting to the arduino on your serial ports. (pyserial required)
 - hides all of the serial communications to the arduino
 - has mirror functions to talk with arduino-attached devices transparently
 
Python libraries for I2C devices: 
 - I2C - ISL29125 RGB Sensor
 - I2C - MCP23017 16 bit IO expander
 - I2C - PCF8574 8 bit IO expander
 
Additional Python support:
 - millis() and delay() for Arduino-like programs
 - serial port simulator mode for when you forgot your arduino at home
 - I2C probe routine to see what's out there
 - Gamma curve adapter for LED intensity
 
-- 

The primary use of this is to have a desktop python script interact with a RC2014 Bus Supervisor board,
which can control the Z80's bus via I2C.  With this Arduino script, and the included python interface,
you can completely command the Z80; read/writing the RAM, ROM, perform IO, etc.
