//////////////////////////////////////////////////////////////
// strand
//
//  All of the LED Strand interaction routines
//

#include <Adafruit_WS2801.h>
#include "cfg.h"

#define kMaxPixel  (7)

#ifdef __LEONARDO__ /* SS Micro, etc */
#define kDataPin   (14) /* WHITE */
#define kClockPin  (15) /* GREEN */
#endif

#ifdef __PRO_MICRO__ /* Nano V3, etc */
#define kDataPin   (11) /* WHITE */
#define kClockPin  (12) /* GREEN */
#endif

Adafruit_WS2801 strand = Adafruit_WS2801( kMaxPixel, kDataPin, kClockPin );

//////////////////////////////////////////////////
// every module has a Setup, and poll

static long strandTimeout = 0;
static bool enableStrandIndicator = false;

void strandSetup()
{
  /* start it up, clear it */
  strand.begin();
  strandAllOff();

  /* indicate our version as a color */
  strandIndicatorEnable();
  strandIndicator( 2000, kVersionColor );  /* startup ID color */
  enableStrandIndicator = false;
  strandIndicatorDisable();
}

void strandPoll()
{
  if ( (strandTimeout > 0) && (millis() > strandTimeout) ) {
    strandAllOff();
    strandTimeout = 0;
  }
}

void strandIndicatorEnable( void )
{
  enableStrandIndicator = true;
  strandIndicator( kDuration_Gen, kColor_IndGenOn );
}

void strandIndicatorDisable( void )
{
  enableStrandIndicator = true;
  strandIndicator( kDuration_Gen, kColor_IndGenOff );
  enableStrandIndicator = false;
}

void strandIndicator( long durationMS, byte r, byte g, byte b)
{
  if ( !enableStrandIndicator ) return;

  strandSetRGB( 0,  r, g, b );
  strandShow();
  strandTimeout = millis() + durationMS;
}


//////////////////////////////////////////////////
// interactions

// Create a 24 bit color value from R,G,B
uint32_t strandColor(byte r, byte g, byte b)
{
  uint32_t c;
  c = r;
  c <<= 8;
  c |= g;
  c <<= 8;
  c |= b;
  return c;
}

void strandSetRGB( int idx, byte rr, byte gg, byte bb )
{
  if ( idx < 0 || idx > kMaxPixel ) return;

  strand.setPixelColor( idx, strandColor( rr, gg, bb ));
}

void strandSetColor( int idx, uint32_t color )
{
  if ( idx < 0 || idx > kMaxPixel ) return;

  strand.setPixelColor( idx, color );
}

void strandShow( void )
{
  strand.show();
}


void strandAllColor( uint32_t color )
{
  int i;

  for ( i = 0 ; i < kMaxPixel ; i++ ) {
    strand.setPixelColor( i, color );
  }
  strand.show();
}

void strandAllOff( void )
{
  strandAllColor( 0x000000 );
}

