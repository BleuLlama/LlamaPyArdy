#!/usr/bin/python
################################################################################
# this code has been adapted from:
# 	SparkFunISL29125
# 	Jordan McConnell @ SparkFun Electronics
#	25 Mar 2014
#	https://github.com/sparkfun/ISL29125_Breakout
#	License: "The hardware is released under Creative Commons Share-alike 3.0"
################################################################################

from libArdySer import ArdySer
from lib_GenericChip import GenericChip
from GS_Timing import delay

class ISL29125_RGBSensor(GenericChip):

##################################
# Constants

	# I2C Address (8-bit)
	I2C_ADDR      = 0x44

	# Registers
	DEVICE_ID     = 0x00
	CONFIG_1      = 0x01
	CONFIG_2      = 0x02
	CONFIG_3      = 0x03
	THRESHOLD_LL  = 0x04
	THRESHOLD_LH  = 0x05
	THRESHOLD_HL  = 0x06
	THRESHOLD_HH  = 0x07
	STATUS        = 0x08 
	GREEN_L       = 0x09 
	GREEN_H       = 0x0A
	RED_L         = 0x0B
	RED_H         = 0x0C
	BLUE_L        = 0x0D
	BLUE_H        = 0x0E

	# Configuration Settings
	CFG_DEFAULT  = 0x00

	# CONFIG1
	#  Pick a mode, determines what color[s] the sensor samples, if any
	CFG1_MODE_POWERDOWN  = 0x00
	CFG1_MODE_G          = 0x01
	CFG1_MODE_R          = 0x02
	CFG1_MODE_B          = 0x03
	CFG1_MODE_STANDBY    = 0x04
	CFG1_MODE_RGB        = 0x05
	CFG1_MODE_RG         = 0x06
	CFG1_MODE_GB         = 0x07

	# Light intensity range
	#  In a dark environment 375Lux is best, otherwise 10KLux is likely the best option
	CFG1_375LUX  = 0x00
	CFG1_10KLUX  = 0x08

	# Change this to 12 bit if you want less accuracy, but faster sensor reads
	#  At default 16 bit, each sensor sample for a given color is about ~100ms
	CFG1_16BIT   = 0x00
	CFG1_12BIT   = 0x10

	# Unless you want the interrupt pin to be an input that triggers sensor sampling, leave this on normal
	CFG1_ADC_SYNC_NORMAL  = 0x00
	CFG1_ADC_SYNC_TO_INT  = 0x20

	# CONFIG2
	#  Selects upper or lower range of IR filtering
	CFG2_IR_OFFSET_OFF  = 0x00
	CFG2_IR_OFFSET_ON   = 0x80

	# Sets amount of IR filtering, can use these presets or any value between 0x00 and 0x3F
	#  Consult datasheet for detailed IR filtering calibration
	CFG2_IR_ADJUST_LOW   = 0x00
	CFG2_IR_ADJUST_MID   = 0x20
	CFG2_IR_ADJUST_HIGH  = 0x3F

	# CONFIG3
	#  No interrupts, or interrupts based on a selected color
	CFG3_NO_INT  = 0x00
	CFG3_G_INT   = 0x01
	CFG3_R_INT   = 0x02
	CFG3_B_INT   = 0x03

	# How many times a sensor sample must hit a threshold before triggering an interrupt
	# More consecutive samples means more times between interrupts, but less triggers from short transients
	CFG3_INT_PRST1  = 0x00
	CFG3_INT_PRST2  = 0x04
	CFG3_INT_PRST4  = 0x08
	CFG3_INT_PRST8  = 0x0C

	# If you would rather have interrupts trigger when a sensor sampling is complete, enable this
	# If this is disabled, interrupts are based on comparing sensor data to threshold settings
	CFG3_RGB_CONV_TO_INT_DISABLE  = 0x00
	CFG3_RGB_CONV_TO_INT_ENABLE   = 0x10

	# STATUS FLAG MASKS
	FLAG_INT        = 0x01
	FLAG_CONV_DONE  = 0x02
	FLAG_BROWNOUT   = 0x04
	FLAG_CONV_G     = 0x10
	FLAG_CONV_R     = 0x20
	FLAG_CONV_B     = 0x30


##################################
# Class variables

	# no additional from the parent

##################################
# Initialization

	# use the default constructor from the parent
	
	def initChip( self ):
		deviceID = self.ardy.i2cRead8( self.i2cAddr8, self.DEVICE_ID )
		print( "RGB Device ID is: 0x{:02x}".format( deviceID ) )

		self.reset()
		
		self.config( self.CFG1_MODE_RGB | self.CFG1_10KLUX,
					 self.CFG2_IR_ADJUST_HIGH,
					 self.CFG_DEFAULT )
		delay( 500 )
		
		
	def reset( self ):
		#reset registers
		self.ardy.i2cWrite8( self.i2cAddr8, self.DEVICE_ID, 0x46 ) #?

		# check reset
		data  = self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_1 )	# cfg1 
		data |= self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_2 )	# cfg2 
		data |= self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_3 )	# cfg3 
		data |= self.ardy.i2cRead8( self.i2cAddr8, self.STATUS   )	# status

		if not data is 0x00:
			print "Reset failed."
		else:
			print "Reset ok."


	def config( self, cfg1, cfg2, cfg3 ):
		# set the 3 config registers
		self.ardy.i2cWrite8( self.i2cAddr8, self.CONFIG_1, cfg1 )
		self.ardy.i2cWrite8( self.i2cAddr8, self.CONFIG_2, cfg2 )
		self.ardy.i2cWrite8( self.i2cAddr8, self.CONFIG_3, cfg3 )

		data = self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_1 )
		if not data is cfg1:
			print "Config 1: failed"

		data = self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_2 )
		if not data is cfg2:
			print "Config 2: failed"

		data = self.ardy.i2cRead8( self.i2cAddr8, self.CONFIG_3 )
		if not data is cfg3:
			print "Config 3: failed"


	##################################
	# Interface

	def Get( self ):
		red   = self.ardy.i2cRead16( self.i2cAddr8, self.RED_L )
		green = self.ardy.i2cRead16( self.i2cAddr8, self.GREEN_L )
		blue  = self.ardy.i2cRead16( self.i2cAddr8, self.BLUE_L )
		return [ red, green, blue ]


	def GetUnit( self ):
		maxVal = float( 0xFFFF )
		[red, green, blue] = self.Get()

		red   = float( red ) / maxVal
		green = float( green ) / maxVal
		blue  = float( blue ) / maxVal

		return [ red, green, blue ]


	def GetScaledInt( self, scaledMax ):
		[red, green, blue] = self.GetUnit()

		red   = int( red * scaledMax )
		green = int( green * scaledMax )
		blue  = int( blue * scaledMax )

		return [ red, green, blue ]
