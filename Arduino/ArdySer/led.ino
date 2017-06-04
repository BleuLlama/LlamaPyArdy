//////////////////////////////////////////////////////////////
// LED
//
//  LED pattern display
//

#include <avr/pgmspace.h>


uint8_t ledPin = LED_BUILTIN;

// depend on whether the LED is sourced or sinked, the
// sense of it will be backwards
#undef kLEDPinSourced

#ifdef kLEDPinSourced
#define kLEDOn  HIGH
#define kLEDOff LOW
#else
#define kLEDOn  LOW
#define kLEDOff HIGH
#endif


//////////////////////////////////////////////////

// patterns are a bitfield, and are stepped through from left
// to right,  eg 0x80, 0x40, 0x20, 0x10...
// if the millisPerStep is set at 100, then all 8 steps will hapen
// in 100*8 = 800 milliseconds = 0.8s
const uint8_t patterns[] PROGMEM = {
  B00000000,  // off
  B11111111,  // on
  B01010101,  // fast blink
  B11001100,  // medium blink
  B11110000,  // slow blink
  B01111111,  // blip 0
  B10000000,  // blip 1
};

#define kLEDPatternOff   (0)
#define kLEDPatternOn    (1)
#define kLEDPatternFast  (2)
#define kLEDPatternMed   (3)
#define kLEDPatternSlow  (4)
#define kLEDPatternBlip0 (5)
#define kLEDPatternBlip1 (6)
#define kLEDPatternMax      (6)

#define kLEDPatternDefault  (kLEDPatternMed)

#define kLEDMillisPerStep (100)

//////////////////////////////////////////////////

uint8_t ledPatternWhich = kLEDPatternDefault;
uint8_t ledPatternFrames = 0x00;
uint8_t ledPatternMask = 0x80;
unsigned long ledTimeout = 0;

//////////////////////////////////////////////////
uint8_t ledSetPin( uint8_t newPin )
{
  digitalWrite( ledPin, kLEDOff );
  ledPin = newPin;
  pinMode( ledPin, OUTPUT );

  cfgSet( kEE_LEDPin, newPin );
  return newPin;
}

void ledTimeoutReset()
{
  ledTimeout = millis() + kLEDMillisPerStep;
}

int ledSetPattern( int which )
{
  if ( which > kLEDPatternMax ) which = kLEDPatternDefault;
  if ( which < 0 ) which = kLEDPatternDefault;
  ledPatternWhich = which;

  ledPatternFrames = pgm_read_byte_near( patterns + ledPatternWhich );
  ledTimeoutReset();
  ledPatternMask = 0x80;

  // in case we're off, we force it, since ledPoll will drop it.
  if ( ledPatternWhich == kLEDPatternOff ) {
    digitalWrite( ledPin, kLEDOff );
  }

  // and do a kickoff-poll
  ledPoll();
  return which;
}


//////////////////////////////////////////////////
// every module has a Setup, and poll


// ledSetup
//  clear and setup the led pattern in a known state
void ledSetup()
{
  ledPin = cfgGet( kEE_LEDPin );

  pinMode( ledPin, OUTPUT );
  ledSetPattern( kLEDPatternDefault );
}



// ledPoll
//  check for timeout, adjust pattern/state, drive the LED
void ledPoll()
{
  int writeState = LOW;

  // check to see if we're disabled
  if ( ledPatternWhich == kLEDPatternOff ) return;

  // first check for timeout
  if ( millis() > ledTimeout ) {
    // this step timed out, shift the mask
    ledPatternMask >>= 1;

    // if the mask is clear, reset the mask
    if ( ledPatternMask == 0 ) {
      ledPatternMask = 0x80;
    }

    // and reset the timeout for the next update time
    ledTimeoutReset();
  }

  // determine the current state from the pattern and mask
  if ( ledPatternFrames & ledPatternMask )
    writeState = kLEDOn;
  else
    writeState = kLEDOff;

  // and display the current state!
  digitalWrite( ledPin, writeState );
}

void ledAnimationSentinel( int port )
{
  // disable the LED animation if it's the LED port
  if ( port == ledPin ) {
    ledSetPattern( kLEDPatternOff );
    digitalWrite( ledPin, kLEDOff );
  }
}

