#!/usr/bin/python
################################################################################
#	
#	Llama2c.py
#
#	Main command line interface for the ArdySerial stuff
#	- Creates the Ardy instance
#	- makes the connection to the Ardy
#	- I2c and serial probing
#	- test things?
#
################################################################################
#
#	v001 2017-05-09 SDL initial version

################################################################################
# you may need to install pyserial:
# 	sudo pip install pyserial
# 	on windows, c:\Python27\Scripts\pip.exe install pyserial
################################################################################

################################################################################
# importing libraries...

import sys
sys.dont_write_bytecode = True
sys.path.append( 'devices' )
sys.path.append( 'libs' )

import getopt

# connection
from libArdySer import ArdySer


################################################################################
# signal stuff

import signal

def signal_handler( signal, frame ):
	print( "BREAK." )
	sys.exit( 0 )


# and immediately install it on including this library
signal.signal( signal.SIGINT, signal_handler )
#signal.pause()




################################################################################
# main command line interface routines

class PyArdyApp:

	def usage( self ):
		print "App.py <options>"
		print "	-a TXT  attach to port with 'TXT' matching"
		print "	-l	  List detected serial ports"
		print "	-p	  perform I2C probe"
		print "	-s	  Simulated Arduino connection mode"

	def run( self, ardy ):
		print "replace this function."


	def main( self, argv ):
		ardy = ArdySer( True )

		doI2cProbe = False
		arduinotext = None

		try:
			opts, args = getopt.getopt(argv,"hlspa:",["arduino="])

		except getopt.GetoptError:
			self.usage()
			sys.exit(2)

		for opt, arg in opts:
			if opt == '-l':
				ardy.listSerialPorts()
				return

			elif opt == '-s':
				ardy.EnableSimulation()

			elif opt == '-p':
				doI2cProbe = True

			elif opt == '-a':
				arduinotext = arg

			elif opt in ("-a", "--arduino"):
				arduinotext = arg

			else:
				self.usage()
				sys.exit()

			ardy.openConnection( arduinotext )

			if not ardy.isConnected():
				print " ===================="
				print "  Arduino not found!"
				print " ===================="
				print
				self.usage()
				return

			if doI2cProbe is True:
				ardy.i2cProbe()
				return
			
			self.run( ardy )

# put this in your main app as well.
#if __name__ == "__main__":
#		paa = PyArdyApp()
#		paa.main(sys.argv[1:])
