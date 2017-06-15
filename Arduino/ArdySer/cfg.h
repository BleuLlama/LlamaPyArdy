#ifndef __CFG_H__
#define __CFG_H__

/////////////////////////////////////////////////////////////////
// Version info
#define kCurrentVersion 0x0005

#define kVersionColor  0, 64, 64

//  v005 - 2017-06-13  Indicator Mode for strand
//
//  v004 - 2017-05-28  Servo  (0, 64, 0)
//
//  v003 - 2017-05-23  strand support
//
//  v002 - 2017-05-12  Added "NoRegister" read/write
//
//  v001 - 2017-05-02  initial version
//


/////////////////////////////////////////////////////////////////
/// platform/pin usage:

#define __LEONARDO__ (1)
//  14 - WS2801 Strand Data (White)
//  15 - WS2801 Strand Clock (Green)


//#define __PRO_MICRO__ (1)
//  11 - WS2801 Strand Data (White)
//  12 - WS2801 Strand Clock (Green)


/////////////////////////////////////////////////////////////////
// Serial

#define kBaudRate (115200)

/////////////////////////////////////////////////////////////////
// Indicator Colors

#define kDuration_I2c   (100)
#define kColor_I2CRead  0,64,0
#define kColor_I2CWrite 64,0,0

#define kDuration_Gen    (500)
#define kColor_IndGenOn  0,0,64
#define kColor_IndGenOff 64,64,0

#endif
