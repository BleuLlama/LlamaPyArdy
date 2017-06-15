#!/usr/bin/python
################################################################################
#	
#	Demos.py
#
################################################################################

################################################################################
# importing libraries...

import sys
sys.dont_write_bytecode = True
sys.path.append( 'devices' )
sys.path.append( 'libs' )

import getopt

# interface handler...
#from libPyArdyApp import PyArdyApp
import libPyArdyApp

# connection
from libArdySer import ArdySer

# support libraries
import GS_Timing
from GS_Timing import delay,micros,millis
from random import random,randint
from libGamma import LlamaGamma

# devices

class I2cScan( libPyArdyApp.PyArdyApp ):

################################################################################
	# main run

	def run( self, ardy ):
		print "..."

################################################################################

# put this in your main app as well.
if __name__ == "__main__":
        da = I2cScan()
        da.main( ['-p'] )
