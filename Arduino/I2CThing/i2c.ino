//////////////////////////////////////////////////////////////
// i2c
//
//  All of the i2c interaction routines
//

#include <Wire.h>

//////////////////////////////////////////////////
// every module has a Setup, and poll

void i2cSetup()
{
  Wire.begin();
}

void i2cPoll()
{
}

//////////////////////////////////////////////////
// some of these originated in the library for the ISL29125 RGB LED Sensor

//////////////////////////////////////////////////
// I2C READ ROUTINES

// Generic I2C read register (single byte)
uint8_t i2cRead8( uint8_t address, uint8_t reg )
{
  Wire.beginTransmission(address);
  Wire.write(reg);
  Wire.endTransmission();
  Wire.beginTransmission(address);
  Wire.requestFrom(address, (uint8_t)1);
  uint8_t data = Wire.read();
  Wire.endTransmission();

  return data;
}

// Generic I2C write data to register (single byte)
void i2cWrite8( uint8_t address, uint8_t reg, uint8_t data )
{
  Wire.beginTransmission(address);
  Wire.write(reg);
  Wire.write(data);
  Wire.endTransmission();

  return;
}


// Generic I2C read register (single byte)
uint8_t i2cRead8NoReg( uint8_t address )
{
  Wire.beginTransmission(address);
  Wire.requestFrom(address, (uint8_t)1);
  uint8_t data = Wire.read();
  Wire.endTransmission();

  return data;
}


//////////////////////////////////////////////////
// I2C WRITE ROUTINES

// Generic I2C read registers (two bytes, LSB first)
uint16_t i2cRead16( uint8_t address, uint8_t reg )
{
  uint16_t data = 0x0000;

  Wire.beginTransmission(address);
  Wire.write(reg);
  Wire.endTransmission();

  Wire.beginTransmission(address);
  Wire.requestFrom(address, (uint8_t)2); // request 2 bytes of data
  data = Wire.read();
  data |= (Wire.read() << 8);
  Wire.endTransmission();

  return data;
}

// Generic I2C write data to registers (two bytes, LSB first)
void i2cWrite16( uint8_t address, uint8_t reg, uint16_t data )
{
  Wire.beginTransmission(address);
  Wire.write(reg);
  Wire.write(data);
  Wire.write(data >> 8);
}

// Generic I2C write data to no register (single byte)
void i2cWrite8NoReg( uint8_t address, uint8_t data )
{
  Wire.beginTransmission(address);
  Wire.write(data);
  Wire.endTransmission();
}
