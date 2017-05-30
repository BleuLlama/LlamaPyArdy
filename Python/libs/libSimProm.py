#!/usr/bin/python

import sys, getopt

################################################################################
# Fake EEPROM simulation
class SimProm:
    eeprom = None 
    eepromSz = 0
    
    def __init__( self ):
	self.create()

    def create( self ):
	# initialize the rom
	self.eepromSz = 512
	self.eeprom = bytearray(b'\xEE' * self.eepromSz)

	# pre-load with known valid values
	self.Set(  0, 0xbe )	# sentinel
	self.Set(  1, 0xef )
	self.Set(  8, 0x80 )	# version
	self.Set(  9, 0x80 )
	self.Set( 10, 13 )	# led pin
	return


    ##############################

    def Get( self, addr ):
	addr = int( addr )
	print "EEPROM Get {}".format( addr )
	if addr > self.eepromSz:
		return 0xFF;

	return self.eeprom[addr]


    def Set( self, addr, val ):
	addr = int( addr )
	val = int( val )
	if addr > self.eepromSz:
		return;

	self.eeprom[addr] = val
	return
