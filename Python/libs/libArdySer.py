#!/usr/bin/python

import sys
import glob
import serial
import serial.tools.list_ports
from time import sleep
import sys, getopt
import datetime
from GS_Timing import millis, delay
from libSimCom import SimCom

# pip install pyserial
# on windows, c:\Python27\Scripts\pip.exe

################################################################################

class ArdySer:

    deviceport = None	# the serial port we're connected to
    comport = None	# the opened device handle
    simulation = False	# are we running on "simulated" hardware?
    unreadCharacter = None # for our read/unread

    def __init__( self, verbose = False ):
	self.verbose = verbose
	self.comport = None
	self.deviceport = None
	self.simulation = False

    def GetPortName( self ):
	if self.deviceport is None:
		return "(none)"
	else:
		return self.deviceport.device

    def GetPortDescription( self ):
	if self.deviceport is None:
		return "(none)"
	else:
		return self.deviceport.description

    def EnableSimulation( self ):
	print "Enabling ArdySer Simulation mode..."
	self.simulation = True

################################################################################
# port discovery

    def couldBeArduino( self, trycomport ):
	possibilities = ['Arduino', 'CH340', 'wchusb' ]
	for needle in possibilities:
	    if needle in trycomport.description:
		    return True
	    if needle in trycomport.device:
		    return True
	# nope
	return False


    def detectArduinoPort( self, usrsearch ):
	theArduino = None;

	if self.simulation is True:
	    return SimCom	# it is the port and the sim.
	
	ports = list(serial.tools.list_ports.comports())

	for tryComPort in ports:
	    if usrsearch is None:
		# only check the builtins
		if self.couldBeArduino( tryComPort ):
		    #print "Arduino on " + p.device
		    theArduino = tryComPort
	    else:
		# only check the usrsearch
		if usrsearch in tryComPort.description:
		    #print "Requested port found on " + p.device
		    theArduino = tryComPort
		if usrsearch in tryComPort.device:
		    #print "Requested port found on " + p.device
		    theArduino = tryComPort
	return theArduino;


    def listSerialPorts( self ):
	print ""
	print "Serial ports: " 
	#print serial_ports()
	print ""
	ports = list(serial.tools.list_ports.comports())
	if len( ports ) == 0:
	    print "   No ports found."
	    return

	for p in ports:
	    additional = ""
	    if( self.couldBeArduino( p )):
		additional = " (detected as Arduino)"
	    print "   " + p.device + " -- " + p.description + additional

################################################################################
# utility

    def vprint( self, text ):
	if self.verbose and not text is None:
		print text;

    def i2cProbe( self ):
	print "Scanning I2C..."

	#  only need to scan bottom half, since it's 7bit address
	x = 0
	lastWasdot = False
	for i in range( 0x00, 0x80 ):

	    # read device id
	    self.i2cWrite8( i, 0x00, 0x00 )
	    self.i2cWrite8( i, 0x01, 0x00 )
	    self.i2cWrite8( i, 0x02, 0x00 )
	    self.i2cWrite8( i, 0x03, 0x00 )
	
	    value0 = self.i2cRead8( i, 0x00 )
	    value1 = self.i2cRead8( i, 0x01 )
	    if value0 is not 0xff or value1 is not 0xff:
		if lastWasDot is True:
			print 
		print "0x{:02x}: Detected.  (0x{:02x})".format( i, value0 )
		lastWasDot = False
		x = 0
	    else:
		# one dot per address checked
		sys.stdout.write( "." )
		sys.stdout.flush()
		# print a newline every 64 chars
		if x is 64:
		    print # newline
		    x = 0;
		x = x + 1
		lastWasDot = True
	    
	

################################################################################
# serial port layer

    def isConnected( self ):
	if self.comport is None:
		return False
	return True


    def closeConnection( self ):
	if self.isConnected():
	    self.comport.close()
	self.comport = None
	self.deviceport = None
	self.unreadCharacter = None;


    def openConnection( self, searchTerm = None ):
	if not self.isConnected():
		self.closeConnection()

	self.deviceport = self.detectArduinoPort( searchTerm )

	if self.deviceport is None:
		return

	self.vprint( "Serial port: " + self.deviceport.device )

	if( self.deviceport.device == SimCom.SimDevice ):
		self.comport = SimCom()
	else:
		self.comport = serial.Serial( self.deviceport.device, 115200, timeout=10 )
	self.comport.close()
	self.comport.open()

	self.flush()

	widgetVersion = self.getVersion()
	self.vprint( "Connected to version {:04x}".format( widgetVersion ))
	siga = self.configRead( 0 )
	sigb = self.configRead( 1 )
	self.vprint( "  Signature: {:02x} {:02x}".format( siga, sigb ))

    def flush( self ):
	self.unreadCharacter = None;
	# need to revisit this...
	self.comport.flush()
	delay( 4 )
	self.comport.flushInput()
	self.comport.flushOutput()
	delay( 4 )
	# if using 3.0 of pyserial:
	#self.comport.reset_input_buffer();
	#self.comport.reset_output_buffer();


    def send( self, text ):
	if not self.isConnected():
		return
	self.comport.write( text );
	#self.vprint( "Sending: |" + text + "|" )

    def sendln( self, text ):
	self.send( text )
	self.send( "\n" )

    def sendList( self, list ):
	sendstr = ','.join( str(item) for item in list )
	self.sendln( sendstr )



    def our_read( self ):
	if not self.unreadCharacter == None:
	    ch = self.unreadCharacter
	    self.unreadCharacter = None
	    return ch

	if not self.isConnected():
	    return '';

	return self.comport.read( 1 )

    def our_unread( self, ch ):
	self.unreadCharacter = ch

    def our_consumeNewlines( self ):
	while True:
	    # read a character until it's not a newline
	    # then unread it.
	    ch = self.our_read()
	    if ch != '\n' and ch != '\r':
		self.our_unread( ch )
		break

    # read a line of content from the serial port
    # returns the line, without 
    def readln( self ):
	if not self.isConnected():
		return "=0xFFFF"

	linetxt = ""
	while True:
	    c = self.our_read()
	    if (c == '\n') or (c == '\r'):
		self.our_consumeNewlines();
		break

	    linetxt += c

	return linetxt


################################################################################
# serial port layer

######################################## 
# Misc stuff

    def getVersion( self ):
	self.flush()
	self.sendList( [ "ver" ] )
	junk = self.readln() # echoback
    	return self.retvalToInt( self.readln() )

    def configRead( self, key ):
	self.flush()
	self.sendList( [ "cr", key ] )
	junk = self.readln() # echoback
    	return self.retvalToInt( self.readln() )

    def configWrite( self, key, value ):
	self.flush()
	self.sendList( [ "cw", key, value ] )
	junk = self.readln() # echoback

######################################## 
# LED pattern stuff

    def ledPattern( self, value ):
	self.flush()
	self.sendList( [ "lp", value ] )
	junk = self.readln() # echoback

    def ledPin( self, pin ):
	self.flush()
	self.sendList( [ "ls", pin ] )
	junk = self.readln() # echoback

######################################## 
# Pin IO pattern stuff
    def retvalToInt( self, retval ):
	retint = 0
	try:
	    retval = retval[1:]	# "0x0001"
	    retint = int( retval, 16 )
	except:
	    return 0xFFFF
	    pass
	return retint

    def _commonWrite( self, which, pin, value ):
	self.flush()
	self.sendList( [ which, pin, value ] )
	junk = self.readln() # echoback

    def digitalWrite( self, pin, value ):
	return self._commonWrite( "dw", pin, value )

    def analogWrite( self, pin, value ):
	return self._commonWrite( "aw", pin, value )


    def _commonRead( self, cmd, pin ):
	self.flush()
	self.sendList( [ cmd, pin ] )
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() )

    def digitalRead( self, pin ):
	return self._commonRead( "dr", pin )

    def analogRead( self, pin ):
	return self._commonRead( "ar", pin )


######################################## 
# I2C stuff

    def _commonI2cWrite( self, valsize, device, register8, value ):
	self.sendList( [ "iw", valsize, device, register8, value ] )
	value = self.readln() # echoback

    def i2cWrite8( self, device, register8, value8 ):
	self._commonI2cWrite( 8, device, register8, value8 );

    def i2cWrite16( self, device, register8, value16 ):
	self._commonI2cWrite( 16, device, register8, value8 );


    def i2cWrite8NoReg( self, device, value8 ):
	self.sendList( [ "iwnr", 8, device, value8 ] )
	value = self.readln() # echoback


    def _commonI2cRead( self, valsize, device, register8 ):
	retvalue = 0xFFFF

	self.flush()
	self.sendList( [ "ir", valsize, device, register8 ] )
	delay( 5 )
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() ) # get the value "=0x0001"
	

    def i2cRead8( self, device, register8 ):
	return self._commonI2cRead( 8, device, register8 )

    def i2cRead16( self, device, register8 ):
	return self._commonI2cRead( 16, device, register8 )


######################################## 
# Servo stuff

    def servoStart( self, pin ):
	self.flush()
	self.sendList( [ "sv", pin, "start" ] )
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() )
	    
    def servoEnd( self, pin ):
	self.flush()
	self.sendList( [ "sv", pin, "end" ] )
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() )
	    
    def servoWrite( self, pin, value ):
	self.flush()
	self.sendList( [ "sv", pin, value ] )
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() )


######################################## 
# LED Strand stuff

    def strandColor( self, idx, r, g, b ):
	self.flush()
	self.sendList( [ "st", idx, r, g, b ] );
	value = self.readln() # echoback
	return self.retvalToInt( self.readln() )

    def strandShow( self ):
	self.flush()
	self.sendList( [ "st", "now" ] );
	return self.retvalToInt( self.readln() )

    def strandOff( self ):
	self.flush()
	self.sendList( [ "st", "off" ] );
	return self.retvalToInt( self.readln() )
