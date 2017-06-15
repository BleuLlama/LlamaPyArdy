//////////////////////////////////////////////////////////////
// ArdySer
//
//  Serial-to-I2C/PinIO thing
//   yorgle@gmail.com
//
// Version information in "cfg.h"
#include "cfg.h"



//////////////////////////////////////////////////
// setup
//  call all of the init functions in all of our modules

void setup()
{
  serSetup();
  cfgSetup();
  strandSetup();
  ledSetup();
  lineSetup();
  i2cSetup();
}

//////////////////////////////////////////////////////////////
// loop
//  round-robin poll all of the modules

void loop()
{
  serPoll();
  strandPoll();
  ledPoll();
  linePoll();
  i2cPoll();
}

