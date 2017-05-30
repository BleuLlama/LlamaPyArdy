//////////////////////////////////////////////////////////////
// line
//
//  handle a line coming from the serial system
//

#include <Servo.h>
Servo servo3, servo5, servo6, servo9, servo10;

//////////////////////////////////////////////////
// every module has an init, and poll

void lineSetup()
{
}

void linePoll()
{
  // nothing happens here
  // execution is transferred via Serial
}


//////////////////////////////////////////////////


/*  Arg vector handlers
     and string manipulations
*/
/* arg vector splitter */
#define kMaxArgs (16)
char * argv[kMaxArgs];
int argc;

void argvClear( void )
{
  for ( int i = 0 ; i < kMaxArgs ; i++ ) {
    argv[i] = NULL;
  }
  argc = 0;
}

int isWhitespace( char ch )
{
  if ( ch == ' ' ) return true;
  if ( ch == '\t' ) return true;
  if ( ch == '\r' ) return true;
  if ( ch == '\n' ) return true;
  return false;
}

char * strClean( char * in )
{
  int pos = 0;

  // trim the front
  while ( isWhitespace( *in )) {
    in++;
  }

  // trim the back
  while ( isWhitespace( in[ strlen( in ) - 1] )  ) {
    in[strlen( in ) - 1] = '\0';
  }
  return in;
}

int argvSplit( char * buf )
{
  char * p;

  argvClear();
  p = strtok( buf, "," );
  while ( p != NULL && argc < kMaxArgs) {
    argv[argc] = strClean(p);
    argc++;
    p = strtok( NULL, "," );
  }

  return argc;
}


/* ************************************** */

// if we can, convert the number string to an int
// otherwise, return 0
int numberArgToInt( int idx )
{
  if ( idx < 0 || idx > kMaxArgs ) return 0;

  if ( argv[idx] == NULL ) return 0;

  // use strtol so it will autoconvert 0x... or ....
  return (int)strtol( argv[idx], NULL, 0 );
}

/* ************************************** */

void lineHandle( char * lbuffer )
{
  int value;
  char result[16];

  if ( !lbuffer || lbuffer[0] == '\0' ) return;

  // local echo
  Serial.print( "< " );
  Serial.println( lbuffer );

  // split the line into comma separated arguments
  argvSplit( lbuffer );

  // make sure it makes sense
  if ( argv[0] == '\0' ) return;

  // ? is help
  if ( !strcmp( argv[0], "?")) {
    Serial.print( F("\nI2C Thing v004\n"
                    "Prefix values with '0x' for HEX\n"
                    "PinIO:\n"
                    "  dw,N,V   digital write port N\n"
                    "  dr,N     digital read port N\n"
                    "  aw,N,V   analog write value to PWM pin N\n"
                    "  ar,N     analog read value on Analog Pin N\n"
                    "  \n"
                    "I2C:\n"
                    "  iw,8,DD,RR,VV     write VV, 1 byte to device D, reg R\n"
                    "  iw,16,DD,RR,VVVV  write VVVV, 2 bytes to device D, reg R\n"
                    "  iwnr,8,DD,VV      write VV, 1 byte to device D\n"
                    "  ir,8,DD,RR        read 1 byte from device D, reg R\n"
                    "  ir,16,DD,RR       read 2 byte from device D, reg R\n"
                    "  irnr,8,DD         read 1 byte to device D\n"
                    "  \n"
                    "LED:\n"
                    "  lp,V        Run pattern V on the LED\n"
                    "  ls,V        Set the LED pin\n"
                    "  st,off      Turn all strand LEDs off\n"
                    "  st,I,R,G,B  Set LED I to be of value R,G,B (0..255)\n"
                    "  st,now      display all set LEDs\n"
                    "Servo:\n"
                    "  sv,N,start   Attach servo stuff to pin N\n"
                    "  sv,N,end     Detach servo stuff from pin N\n"
                    "  sv,N,V       Set servo N at value V\n"
                    "Misc:\n"
                    "  ver      return the current version\n"
                    "  cr,K     read the value in cfg[K]\n"
                    "  cw,K,V   write the key-value in cfg[K]\n"
                    "  \n"
                   ) );
  }

  /* for pinio */
#define kArg_PIN     (numberArgToInt( 1 ))
#define kArg_VALUE   (numberArgToInt( 2 ))

  /* for I2c */
#define kArg_WIDTH   (numberArgToInt( 1 ))
#define kArg_ADDR    (numberArgToInt( 2 ))
#define kArg_REG     (numberArgToInt( 3 ))
#define kArg_VAL     (numberArgToInt( 4 ))

#define kArg_NRVAL   (numberArgToInt( 3 ))

  /* for LED */
#define kArg_PATTERN (numberArgToInt( 1 ))

  /* for EEP */
#define kArg_EEKEY   (numberArgToInt( 1 ))
#define kArg_EEVAL   (numberArgToInt( 2 ))

  /* for strand */
#define kArg_INDEX   (numberArgToInt( 1 ))
#define kArg_RED     (numberArgToInt( 2 ))
#define kArg_GREEN   (numberArgToInt( 3 ))
#define kArg_BLUE    (numberArgToInt( 4 ))

  result[0] = '=';  // pre-loading this as a flag that it was successful

  // I2C
  if ( !strcmp( argv[0], "iw" )) {
    // I2C Write
    if ( kArg_WIDTH == 16 ) {
      i2cWrite16( kArg_ADDR, kArg_REG, kArg_VAL );
      value = kArg_VAL;
    } else {
      i2cWrite8( kArg_ADDR, kArg_REG, kArg_VAL );
    }
    value = kArg_VAL;
  }

  if ( !strcmp( argv[0], "iwnr" )) {
    // I2C Write/ A
    if ( kArg_WIDTH == 8 ) {
      i2cWrite8NoReg( kArg_ADDR, kArg_NRVAL );
      value = kArg_VAL;
    } else {
      // unsupported
    }
    value = kArg_VAL;
  }


  else if ( !strcmp( argv[0], "ir" )) {
    // I2C Read
    if ( kArg_WIDTH == 16 ) {
      value = i2cRead16( kArg_ADDR, kArg_REG );

    } else {
      value = i2cRead8( kArg_ADDR, kArg_REG );
    }
  }

  else if ( !strcmp( argv[0], "irnr" )) {
    // I2C Read
    if ( kArg_WIDTH == 8 ) {
      value = i2cRead8NoReg( kArg_ADDR );

    } else {
      // unsupported
    }
  }


  // Pin IO
  else if ( !strcmp( argv[0], "dw" )) {
    // Digital Write
    ledAnimationSentinel( kArg_PIN );
    value = kArg_VALUE;
    pinMode( kArg_PIN, OUTPUT );
    digitalWrite( kArg_PIN, value );
  }

  else if ( !strcmp( argv[0], "dr" )) {
    // Digital Read
    ledAnimationSentinel( kArg_PIN );
    value = kArg_VALUE;
    pinMode( kArg_PIN, INPUT );
    value = digitalRead( kArg_PIN );
  }

  else if ( !strcmp( argv[0], "aw" )) {
    // Analog Write
    ledAnimationSentinel( kArg_PIN );
    value = kArg_VALUE;
    pinMode( kArg_PIN, OUTPUT );
    analogWrite( kArg_PIN, value );
  }

  else if ( !strcmp( argv[0], "ar" )) {
    // Analog Read
    // so for this pin specifies the analog pins
    value = kArg_VALUE;
    pinMode( kArg_PIN + PIN_A0, INPUT );
    value = analogRead( kArg_PIN );
  }

  else if ( !strcmp( argv[0], "lp" )) {
    // Set LED pattern
    value = ledSetPattern( numberArgToInt( 1 ) );
  }
  else if ( !strcmp( argv[0], "ls" )) {
    // Set LED pattern
    value = ledSetPin( numberArgToInt( 1 ) );
  }

  else if ( !strcmp( argv[0], "ver" )) {
    value = kCurrentVersion;
  }

  else if ( !strcmp( argv[0], "cr" )) {
    value = cfgGet( kArg_EEKEY );
  }
  else if ( !strcmp( argv[0], "cw" )) {
    value = cfgSet( kArg_EEKEY, kArg_EEVAL );
  }

  else if ( !strcmp( argv[0], "st" )) {
    /* LED Strand function */
    if ( argv[1] == NULL ) {
      value = 0xE0EE;
      strandIdColor();

    } else if ( !strcmp( argv[1], "off" )) {
      value = 0xE000;
      strandAllOff();

    } else if ( !strcmp( argv[1], "now" )) {
      value = 0xE000;
      strandShow();

    } else {
      /* it might be a IRGB input */
      strandSetRGB( kArg_INDEX, kArg_RED, kArg_GREEN, kArg_BLUE );
      value = 0xE000;
    }
  }


  else if ( !strcmp( argv[0], "sv" )) {
    /* Servo interactions */
    if ( !strcmp( argv[2], "start" )) {
      int pin = numberArgToInt( 1 );
      switch ( pin ) {
        case ( 3 ):   servo3.attach(3); break;
        case ( 5 ):   servo5.attach(5); break;
        case ( 6 ):   servo6.attach(6); break;
        case ( 9 ):   servo9.attach(9); break;
        case ( 10 ):  servo10.attach(10); break;
      }
      value = pin;

    } else if ( !strcmp( argv[2], "end" )) {
      int pin = numberArgToInt( 1 );
      switch ( pin ) {
        case ( 3 ):   servo3.detach(); break;
        case ( 5 ):   servo5.detach(); break;
        case ( 6 ):   servo6.detach(); break;
        case ( 9 ):   servo9.detach(); break;
        case ( 10 ):  servo10.detach(); break;
          value = pin;
      }

    } else {
      int angle = numberArgToInt( 2 );
      switch ( numberArgToInt( 1 ) ) {
        case ( 3 ):   servo3.write( angle ); break;
        case ( 5 ):   servo5.write( angle ); break;
        case ( 6 ):   servo6.write( angle ); break;
        case ( 9 ):   servo9.write( angle ); break;
        case ( 10 ):  servo10.write( angle ); break;
      }
      value = angle;
    }
  }


  else {
    // Error.
    strcpy( result, "?ERR" );
  }

  // fill the result buffer with a value
  if ( result[0] != '?' ) {
    sprintf( result, "=0x%04x", value );
  }

  // send out the result
  Serial.println( result );
}

