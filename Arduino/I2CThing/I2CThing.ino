//////////////////////////////////////////////////////////////
// I2C Thing
//
//  Serial-to-I2C/PinIO thing
//   yorgle@gmail.com
//
#define kCurrentVersion 0x0004

//  v004 - 2017-05-28  Servo
//
//  v003 - 2017-05-23  strand support
//
//  v002 - 2017-05-12  Added "NoRegister" read/write
//
//  v001 - 2017-05-02  initial version
//


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

