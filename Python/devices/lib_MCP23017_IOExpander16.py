#!/usr/bin/python
################################################################################
#
# lib_MCP23017_IOExpander16
#
#	Implementation of the MCP23017 16 bit I2C IO expander for 
#	the ArdySerial system
#
#	V001 2017-05-09	sdl
#
################################################################################

from libArdySer import ArdySer
from lib_GenericChip import GenericChip
from GS_Timing import millis, delay

class MCP23017_IOExpander16(GenericChip):

##################################
# Constants
	# I2C Address (8 bit)
	I2C_ADDR  	= 0x20
	# A0,A1,A2 can configure this for 0x40-0x4E (8 bit)

	# Registers

	IODIRA 		= 0x00	# Direction A  1 = input, 0 = Output
	IODIRB 		= 0x01	# Direction B
	IOPOLA 		= 0x02	# Invert A  1 = opposite, 1 = same
	IOPOLB 		= 0x03	# Invert B
	GPINTENA	= 0x04	# Interrupt On Change A  1 = en  0 = dis
	GPINTENB 	= 0x05	# Interrupt On Change B
	DEFVALA		= 0x06	# Def IOC value for compare A
	DEFVALB		= 0x07	# Def IOC value for compare B
	INTCONA		= 0x08	# Interrupt control A  0 = previous val
	INTCONB		= 0x09	# interrupt control B  1 = DEFVAL comp,

	IOCONA		= 0x0a	# configuration A
	IOCONB		= 0x0b	# configuration B
	BANK 	= 0x80	# 0=sequential, 1=banked
	MIRROR	= 0x40	# Int pins mirror bit
	SEQOP	= 0x20	# 0=seq en  1=seq dis
	DISSLW	= 0x10	# Slew rate for SDA (1=en)
	HAEN	= 0x08	# (not for I2C model - always en)
	ODR	= 0x04	# 0 active driver  1 open drain
	INTPOL	= 0x02	# interrupt polarity  1=act.high 0=act.low

	GPPUA		= 0x0c	# enable 100k internal pullup A
	GPPUB		= 0x0d	# enable 100k internal pullup B
	INTFA		= 0x0e	# Interrupt Flag A  1=pin causes interrupt
	INTFB		= 0x0f	# Interrupt Flag B  1=pin causes interrupt
	INTCAPA		= 0x10	# Interrupt Capture A
	INTCAPB		= 0x11	# Interrupt Capture B
	GPIOA		= 0x12	# port data A
	GPIOB		= 0x13	# port data B
	OLATA		= 0x14	# Latch A 
	OLATB		= 0x15	# Latch B 

	# none.

##################################
# Class variables

	# no additional from the parent

##################################
# Initialization

	# use the default constructor from the parent
	
	def initChip( self ):
		self.reset()
		return

	def reset( self ):
		# set up all bits as inputs 
		self.DirectionA( 0xFF )
		self.DirectionB( 0xFF )
		
	def test( self ):
		# set for outputs
		self.DirectionA( 0x00 )
		self.DirectionB( 0x00 )

		# loop for a bit
		for b in range( 0, 15 ):
		    for a in range( 0, 0xFFF ):
			    self.SetA( a & 0x00FF )
			    self.SetB( (a & 0x0FF0)>>4 )
			    delay( 10 )
		
	##################################
	# Interface

	def DirectionA( self, mask ):
		self.i2cWrite8( self.IODIRA, mask )
	
	def DirectionB( self, mask ):
		self.i2cWrite8( self.IODIRB, mask )
	
	def SetA( self, data ):
		self.i2cWrite8( self.GPIOA, data )

	def SetB( self, data ):
		self.i2cWrite8( self.GPIOB, data )

	def GetA( self ):
		return self.i2cRead8( self.GPIOA )

	def GetB( self ):
		return self.i2cRead8( self.GPIOB )

