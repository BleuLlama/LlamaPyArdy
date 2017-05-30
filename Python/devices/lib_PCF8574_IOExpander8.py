#!/usr/bin/python
################################################################################
# lib_PCF8574_IOExpander8
#
#	Implementation of the PCF8574 8 bit I2C IO expander for 
#	the ArdySerial system
#
#	V001 2017-05-09	sdl
#
################################################################################

from libArdySer import ArdySer
from lib_GenericChip import GenericChip
from GS_Timing import millis, delay

class PCF8574_IOExpander8(GenericChip):

##################################
# Constants

	# I2C Address (8 bit)
	I2C_ADDR  = 0x22
	# A0,A1,A2 can configure this for 0x40-0x4E (8 bit)

	# Registers
	DEVICE_ID = 0x00

	# none.

#Okay. this one works a bit weird. Might require code changes on the 
#ardy.  there is no register to request from for it. Just read or 
#write to the device.  
#
#need to check if reading/writing to 0x00 is okay. then it'd require nothing
##
#Needs basically Read8()  Write8()  no args

##################################
# Class variables

	writeData = 0x00

##################################
# Initialization

	# use the default constructor from the parent
	
	def initChip( self ):
		deviceID = self.ardy.i2cRead8( self.i2cAddr8, self.DEVICE_ID )
		print( "PCF8574 ID is: 0x{:02x}".format( deviceID ) )
		self.writeData = 0x00
		return
		

	def test( self ):
		for i in range( 0,100 ):
			print i
                	self.ardy.i2cWrite8NoReg( self.i2cAddr8, 0xFF )
			delay( 200 )
                	self.ardy.i2cWrite8NoReg( self.i2cAddr8, 0x00 )
			delay( 200 )
			
		
	##################################
	# Interface
	
	def Set( self, value ):
	    self.ardy.i2cWrite8NoReg( self.i2cAddr8, value )
	    self.writeData = value
	    return value
	
	def Get( self ):
	    return self.ardy.i2cRead8NoReg( self.i2cAddr8 )



	
