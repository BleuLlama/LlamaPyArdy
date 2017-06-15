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
from lib_ISL29125_RGBSensor import ISL29125_RGBSensor
from lib_PCF8574_IOExpander8 import PCF8574_IOExpander8
from lib_MCP23017_IOExpander16 import MCP23017_IOExpander16


class DemoApp( libPyArdyApp.PyArdyApp ):

################################################################################
	# test ISL and Strand

	def testColorMirror( self, ardy ):
		print "Color mirror!"
		rgb = ISL29125_RGBSensor( ardy )

		counter = 0

		while True:
			[red, green, blue] = rgb.GetScaledInt( 255 )

			print( "{:04d} = 0x{:02x} 0x{:02x} 0x{:02x}".format( counter, red, green, blue ));
			ardy.strandColor( 0, red, green, blue )
			ardy.strandShow()
			ardy.flush()

			counter = counter + 1


	def testISLStrand( self, ardy ):
		print "ISL + strand Test"

		rgb = ISL29125_RGBSensor( ardy )

		settleTime = 50 

		ardy.strandOff()
		delay( 500 )

		for which in range ( 0, 3 ):

			print "idx, r, g, b"
			for i in range( 0, 256 ):
				red = 0
				green = 0
				blue = 0

				if which is 0:
					red = i
				if which is 1:
					green = i
				if which is 2:
					blue = i

				ardy.strandColor( 0, red, green, blue )
				ardy.strandShow()
				delay( settleTime )
				[rr,rg,rb] = rgb.Get()
				ardy.flush()
				print "{},  {}, {}, {}".format( i, rr,rg,rb, )

		ardy.strandOff()
		delay( 500 )
		print ""
		print ""

	################################################################################
	# test the strand LEDs

	def testStrandGamma( self, ardy ):
		gamma = LlamaGamma()

		print "Strand Brightness Gamma test"

		#gamma.dump()

		for j in range( 0, 3 ):

			print "{} up".format( j )
			for i in range( 0, 255 ):
				adj = gamma.adjust( i ) 
				ardy.strandColor( 0, 0, adj, 0 )
				ardy.strandShow()
				delay(1)

			print "{} down".format( j )
			for i in range( 0, 255 ):
				adj = gamma.adjust( 255-i ) 
				ardy.strandColor( 0, 0, adj, 0 )
				ardy.strandShow()
				delay(1)

		ardy.strandOff()


	def testStrand( self, ardy ):
		print "Strand Test"
		print "RGB"
		ardy.strandColor( 0, 255,   0,   0 )
		ardy.strandColor( 1,   0, 255,   0 )
		ardy.strandColor( 2,   0,   0, 255 )
		ardy.strandShow()
		delay( 1000 )
		print "Others"
		ardy.strandColor( 3,   0, 255, 255 )
		ardy.strandColor( 4, 255,   0, 255 )
		ardy.strandColor( 5, 255, 255,   0 )
		ardy.strandColor( 6,  30,  30,  30 )
		ardy.strandShow()
		delay( 1000 )
		ardy.strandOff()
		delay( 500 )

		print "Randoms"
		for a in range( 0,10 ):
			for i in range( 0,7 ):
				rr = randint( 0, 100 )
				gg = randint( 0, 100 )
				bb = randint( 0, 100 )
				ardy.strandColor( i, rr, gg, bb )
				ardy.strandShow()
				delay( 100 )

		print "Ending."
		delay( 100 )
		ardy.strandOff()
		print "Done."


	################################################################################
	# create a MCP and call its test routine

	def testMCP( self, ardy ):
	    print "MCP Test"
	    MCP_Data = 0x21
	    MCP_Addr = 0x23
	    mcp = MCP23017_IOExpander16( ardy, MCP_Data )
	    mcp.test();


	################################################################################
	# create a PCF and call its test routine

	def testPCF( self, ardy ):
	    print "PCF Test"
	    PCF_Ctrl = 0x22
	    pcf = PCF8574_IOExpander8( ardy, PCF_Ctrl )
	    pcf.test();


	################################################################################
	# talk to an ISL color sensor

	def testISL( self, ardy ):
		print "ISL Test"

		rgb = ISL29125_RGBSensor( ardy )

		for i in range( 0, 5 ):
			[r,g,b] = rgb.Get()
			print( "RGB = 0x{:04x} 0x{:04x} 0x{:04x}".format( r,g,b ));
			delay( 1000 )


	################################################################################
	# talk directly to the LED flash loop, bitwise IO, and analog read

	def testLEDsAndIO( self, ardy ):
		ardy.ledPin( 6 );
		ardy.ledPattern( 3 );

		value = ardy.digitalRead( 3 );
		print( "Value read was " + str( value ) )

		for i in range( 0, 3 ):
			value = ardy.analogRead( i );
			print( "{}: Value read was {}".format( i, value ) )
			delay( 200 )

		#for i in range( 0, 255 ):
		#	ardy.analogWrite( 6, i );
		#	delay( 1 );


	################################################################################
	# arcade game tester for lego display

	def randomColorOnLed( self, ardy, gamma, lightno ):
	    colors = [
		[ 0, 0, 0 ],
		[ 1, 0, 0 ],
		[ 0, 1, 0 ],
		[ 0, 0, 1 ],
		[ 1, 1, 0 ],
		[ 1, 0, 1 ],
		[ 0, 1, 1 ]
		]

	    c = randint( 0, 6 )
	    [r,g,b] = colors[c]

	    r = gamma.adjust( int( float( r ) * randint( 0, 255 )))
	    g = gamma.adjust( int( float( g ) * randint( 0, 255 )))
	    b = gamma.adjust( int( float( b ) * randint( 0, 255 )))

	    ardy.strandColor( lightno, r, g, b )
	    

	def testLegoDisplay( self, ardy ):
		gamma = LlamaGamma()
		indexes  = [ 2, 3, 4, 5 ]
		timeouts = [ 0, 0, 0, 0 ]
		flashing = [ False, False, False, False ]

		ardy.strandOff();

		steps = 0
		while True:
			# for each light...
			for a in range( 0, 4 ):

				# Timeouts to pick new color, time, flashing
				if( millis() > timeouts[a] ):
					self.randomColorOnLed( ardy, gamma, indexes[ a ] )
					if random() > 0.5:
						timeouts[ a ] = millis() + randint( 400, 700 )
					else:
						timeouts[ a ] = millis() + randint( 10, 70 )
					if random() > 0.5:
						flashing[ a ] = True
					else:
						flashing[ a ] = False

				steps = steps + 1
				#if flashing[ a ] is True:
				#else:

			ardy.strandShow()


	################################################################################

	def testServo( self, ardy ):
		
		configs = [
			# pin, default, min, max, name
			[ 9, 150, 30, 150, "Mouth" ],
			[ 5, 90,  30, 150, "Neck - Twist" ],
			[ 6, 90,  90, 180, "Neck - Tilt" ],
			]
		
		for cfg in configs:
			pin  = cfg[0]
			idle = cfg[1]
			min  = cfg[2]
			max  = cfg[3]
			txt  = cfg[4]
			
			print "Running Servo {} {}-{} ({}) ".format( pin, min, max, txt )
			
			ardy.servoStart( pin )
			
			for iteration in range( 0,2 ):
				ardy.servoWrite( pin, min )
				delay( 500 )
				ardy.servoWrite( pin, max )
				delay( 500 )
			
			ardy.servoWrite( pin, idle )
			delay( 500 )	
			ardy.servoEnd( pin )
			

	################################################################################
	# Misc tests

	def probeI2C( self, ardy ):
		ardy.i2cProbe()

	
	################################################################################
	# test out stuff

	funcdict = {
	    "probeI2C" : probeI2C,
	    "testPCF" : testPCF,
	    "testMCP" : testMCP,
	    "testISL" : testISL,
	    "testStrand" : testStrand,
	    "testStrandGamma"	: testStrandGamma,
	    "testLEDsAndIO" : testLEDsAndIO,
	    "testISLStrand" : testISLStrand,
	    "testColorMirror" : testColorMirror,
	    "testLegoDisplay" : testLegoDisplay,
	    "testServo" : testServo,
	}

	demoList = [
	    [ '0', "I2C Probe", "probeI2C" ],
	    [ '1', "PCF Test", "testPCF" ],
	    [ '2', "MCP Test", "testMCP" ],
	    [ '3', "ISL Test", "testISL" ],
	    [ '4', "Strand Test", "testStrand" ],
	    [ '5', "Strand Gamma Brightness", "testStrandGamma" ],
	    [ '6', "LEDs and IO", "testLEDsAndIO" ],
	    [ '7', "ISL and strand", "testISLStrand" ],
	    [ '8', "Color Mirror", "testColorMirror" ],
	    [ '9', "Lego Display", "testLegoDisplay" ],
	    [ 'a', "Servo Test", "testServo" ],
	    [ 'q', "Quit", None ],
	]


	def run( self, ardy ):
		name = ardy.GetPortName()
		desc = ardy.GetPortDescription()
		print "Using device {} ({})".format( name, desc )
		ardy.indicatorOn();

		while True:
			print ""
			print "   Pick the demo to run:"

			for item in self.demoList:
				print "     {}: {}".format( item[0], item[1] )

			userinput = raw_input( "? " ).strip()
			print "('{}')".format( userinput )

			for item in self.demoList:
				if userinput is item[0]:
					if( item[2] is None ):
						return
					self.funcdict[ item[2] ]( self, ardy )

################################################################################

# put this in your main app as well.
if __name__ == "__main__":
        da = DemoApp()
        da.main(sys.argv[1:])
