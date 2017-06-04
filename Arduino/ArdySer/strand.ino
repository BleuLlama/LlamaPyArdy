//////////////////////////////////////////////////////////////
// strand
//
//  All of the LED Strand interaction routines
//

#include <Adafruit_WS2801.h>

#define __PRO_MICRO__ (1)

#define kMaxPixel  (7)

#ifdef __LEONARDO__
#define kDataPin   (14) /* WHITE */
#define kClockPin  (15) /* GREEN */
#endif

#ifdef __PRO_MICRO__
#define kDataPin   (11) /* WHITE */
#define kClockPin  (12) /* GREEN */
#endif

Adafruit_WS2801 strand = Adafruit_WS2801( kMaxPixel, kDataPin, kClockPin );

//////////////////////////////////////////////////
// every module has a Setup, and poll

static long strandTimeout = 0;

void strandSetup()
{
  /* start it up, clear it */
  strand.begin();
  strandAllOff();

  strandIdColor();
}

void strandPoll()
{
  if( (strandTimeout > 0) && (millis() > strandTimeout) ) {
    strandAllOff();
    strandTimeout=0;
  }
}

void strandIdColor()
{
  /* turn on the first LED green for 2 seconds on startup */
  strandSetRGB( 0,  0, 64, 0 );
  strandShow();
  strandTimeout = millis() + 2000;
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
  if( idx < 0 || idx > kMaxPixel ) return;
  
  strand.setPixelColor( idx, strandColor( rr, gg, bb ));
}

void strandSetColor( int idx, uint32_t color )
{
  if( idx < 0 || idx > kMaxPixel ) return;
  
  strand.setPixelColor( idx, color );
}

void strandShow( void )
{
  strand.show();
}


void strandAllColor( uint32_t color )
{
  int i;

  for( i=0 ; i<kMaxPixel ; i++ ) {
    strand.setPixelColor( i, color );
  }
  strand.show();
}

void strandAllOff( void )
{
  strandAllColor( 0x000000 );
}

