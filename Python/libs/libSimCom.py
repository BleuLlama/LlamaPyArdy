#!/usr/bin/python

import sys
import glob
from libSimProm import SimProm


################################################################################
# Fake Comport + Arduino simulation
class SimCom:
    SimDevice = "/fake/SIMUDUINO"

    device = SimDevice
    description = "Arduino Serial Simulation"
    isOpen = False
    accumulator = ""
    eeprom = None

    def __init__( self ):
    	self.device = self.SimDevice
    	self.description = "Arduino Serial Simulation"
	self.isOpen = False
	self.flush()
	self.eeprom = SimProm()
	print "Serial simulation mode active."


    ####################
    # fake port interface stuff

    def close( self ):
	self.isOpen = True
	
    def open ( self ):
	self.isOpen = False

    def flush ( self ):
	self.accumulator = ""
	return

    def flushInput ( self ):
	self.flush()
	return

    def flushOutput ( self ):
	self.flush()
	return


    ####################
    # stashed data for return values

    stashedLine = "=0xFFFF\n"

    def stash( self, val ):
	self.stashedLine = "=0x{:04x}\n".format( int( val ))

    ####################

    def handleLine( self ):
	args = self.accumulator.strip().split( "," )
	cmd = args[0]

	##############################	

	if cmd == "ver":
		self.stash( 0xEE )
		return

	if cmd == "cr":
		index = args[1]
		self.stash( self.eeprom.Get( index ))
		return

	if cmd == "cw":
		index = args[1]
		value = args[2]
		self.stash( self.eeprom.Set( index, value ))
		return

	##############################	

	if cmd == "lp":
		pattern = args[1]
		print "SIM: LED pattern set for {}".format( pattern )
		self.stash( pattern )
		return

	if cmd == "ls":
		ledpin = args[1]
		print "SIM: LED set for {}".format( ledpin )
		self.stash( ledpin )
		return

	##############################	

	if cmd == "iwnr":
		sz   = int( args[1] )
		addr = int( args[2] )
		data = int( args[3] )
		print "0x{:02x}.Write: 0x{:02x}".format( addr, data )
		self.stash( data )
		return

	if cmd == "irnr":
		sz   = int( args[1] )
		addr = int( args[2] )
		print "0x{:02x}.Read".format( addr )
		self.stash( 0x00 )
		return

	if cmd == "iw":
		sz   = int( args[1] )
		addr = int( args[2] )
		reg  = int( args[3] )
		data = int( args[4] )
		print "0x{:02x}.Write: [0x{:02x}] = 0x{:02x}".format( addr, reg, data )
		self.stash( data )
		return

	if cmd == "ir":
		sz   = int( args[1] )
		addr = int( args[2] )
		reg  = int( args[3] )
		print "0x{:02x}.Read: [0x{:02x}]".format( addr, reg )
		return

	##############################	

	print "{}: unknown option".format( cmd )
	return


    ####################
    # handle writes to us

    def write ( self, txt ):
	#sys.stdout.write( "SER WR:|" )
	#sys.stdout.write( self.cleanText( txt ))
	#sys.stdout.write( "|" )
	#sys.stdout.flush()
	# we're going to assume the newline is the end of a string.
	self.accumulator = self.accumulator + txt;
	if( '\n' in self.accumulator or '\r' in self.accumulator ):
		self.handleLine()
		self.accumulator = ""
	return


    ####################
    # handle reads from us

    def readLine( self ):
	# do something based on "txt"
	return self.stashedLine
