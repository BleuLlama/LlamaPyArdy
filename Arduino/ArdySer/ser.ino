//////////////////////////////////////////////////////////////
// ser
//
//  All of the direct serial routines
//  these will call line.c when they have a full line
//

//////////////////////////////////////////////////
// every module has a Setup, and poll

#define kCRLF  (0x0D0A)
#define kLFCR  (0x0A0D)

#define kMaxLine  (128)
char lineBuf[kMaxLine];
int lineSz = 0;
bool serialOK = false;

// set up the serial port and line buffer
void serSetup()
{
  long serialTimeout = millis() + 2000; // after this amount of time, give up
  serInitLine();

  //Initialize serial and wait for port to open:
  serialOK = false;
  Serial.begin(115200);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
    if ( millis() > serialTimeout )
    {
      // if we get no serial in the timeout. just continue anyway
      return;
    }
  }

  serialOK = true;
  serInitLine();

  // prints title with ending line break
  Serial.println( F("Ready.") );
  serPrompt();
}

// display the prompt
void serPrompt()
{
  Serial.print( F(">> ") );
}

// initialize/clear the line data
void serInitLine()
{
  lineSz = 0;
  lineBuf[0] = '\0';
}

// check for new serial data
//  newlines cause the line handler to be called
//  CRLF or LFCR are absorbed such that CR, LF, CRLF, LFCR are treated the same way
void serPoll()
{
  static unsigned int lastTwo = 0x0000;
  char c;

  while ( Serial.available() )
  {
    c = Serial.read();
    lastTwo = (lastTwo << 8 ) | c;

    // absorb the second of a CRLF or LFCR pair.
    if ( lastTwo == kCRLF || lastTwo == kLFCR )
    {
      lastTwo = c;  // reset it for consecutive CRLF,CRLF handling
      serInitLine();
      return;
    }

    // handle a regular crlf
    if ( c == '\n' || c == '\r' )
    {
      lineHandle( lineBuf );
      serInitLine();
      serPrompt();
      return;
    }

    if ( lineSz < kMaxLine )
    {
      lineBuf[lineSz] = c;     // add the character
      lineSz++;
      lineBuf[lineSz] = '\0';  // terminate line
    }
  }
}

