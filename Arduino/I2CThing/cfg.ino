//////////////////////////////////////////////////////////////
// cfg
//
//  stored configuration (in EEPROM)
//


//////////////////////////////////////////////////////////////
#include <EEPROM.h>

#define kEE_SENTINEL_0  (0)
#define kEE_SENTINEL_1  (1)
#define kEE_VERS        (8)
#define kEE_LEDPin      (0x10)

void cfgFormat()
{
  int i;

  Serial.print( "# Formatting" );
  for( i = 0 ; i < EEPROM.length() ; i++ ) {
    EEPROM.write( i, 0xff );
    if( (i & 0x1F) == 0x00 ) {
      Serial.write( '.' );
    }
  }
  Serial.println( "Done." );
}


void cfgWriteDefaults()
{
  Serial.println( "# Writing default prefs to EEProm" );
  EEPROM.write( kEE_SENTINEL_0, 0xBE );
  EEPROM.write( kEE_SENTINEL_1, 0xEF );
  EEPROM.write( kEE_VERS,       (kCurrentVersion >>8) & 0x0FF );
  EEPROM.write( kEE_VERS+1,     kCurrentVersion & 0x0FF );
  EEPROM.write( kEE_LEDPin,     LED_BUILTIN );
  Serial.println( "# Done." );
}


void cfgSetup()
{
  bool setDefaults = false;

  if( EEPROM.read( kEE_SENTINEL_0 ) != 0xBE ) setDefaults = true;
  if( EEPROM.read( kEE_SENTINEL_1 ) != 0xEF ) setDefaults = true;
    // could check VERS here also to see if migration is needed
  
  if( setDefaults == true ) {
    cfgWriteDefaults();
  }
}

void cfgPoll()
{
}

uint8_t cfgGet( uint8_t key )
{
  if ( key < 0 || key > EEPROM.length() - 1 ) return 0xFF;
  return EEPROM.read( key );
}

uint8_t cfgSet( uint8_t key, uint8_t value )
{
  if ( key < 0 || key > EEPROM.length() - 1 ) return 0xFF;
  EEPROM.write( key, value );
  return value;
}
