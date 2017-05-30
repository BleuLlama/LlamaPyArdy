#!/usr/bin/python

################################################################################
# lib_Generic_Chip
#
# 	parent class to encapsulate some of the general chip interface
#
################################################################################

import sys, getopt
from libArdySer import ArdySer
from GS_Timing import millis, delay

class GenericChip:

	##################################
	# Constants

	# I2C Address (8 bit)
	I2C_ADDR  = 0xFF

	##################################
	# Class variables

	# our copy of the arduino interface	
	ardy = None
	
	# our i2c address
	i2cAddr8 = None


	##################################
	# Initialization
	
	def __init__( self, _ardy, _i2cAddr8 = None ):
		# set the arduino object
		self.ardy = _ardy
		
		# set the i2c address we talk to
		if _i2cAddr8 is None:
			self.i2cAddr8 = self.I2C_ADDR
		else:
			self.i2cAddr8 = _i2cAddr8
			
		# and initialize the chip
		self.initChip()


	def initChip( self ):
		print( "override this function in your chip" );


	##################################
	# helpers

	def i2cWrite8( self, reg, data ):
		self.ardy.i2cWrite8( self.i2cAddr8, reg, data )

	def i2cRead8( self, reg, data ):
		return self.ardy.i2cRead8( self.i2cAddr8, reg )
