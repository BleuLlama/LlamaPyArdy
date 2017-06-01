#!/usr/bin/python
################################################################################
# Bus Supervisor Interface
#
#	- interfaces to the MCP23017 and PCF8574 IO expander chips
#
#	The logic for this was ported from Dr Scott M. Baker's project:
#	http://www.smbaker.com/z80-retrocomputing-4-bus-supervisor
#
################################################################################

from libArdySer import ArdySer
from lib_GenericChip import GenericChip
from GS_Timing import delay
from lib_MCP23017_IOExpander16 import MCP23017_IOExpander16
from lib_PCF8574_IOExpander8 import PCF8574_IOExpander8

class RC2014_BusSupervisor:

	##################################
	# class variables

	ardy = None

	cpuIoData = None
	# A0-A7 - Data byte
	# B0-B7 - Bus control
	M1     = 0x01	# B0
	CLK    = 0x02	# B1
	INT    = 0x04	# B2
	MREQ   = 0x08	# B3
	WR     = 0x10	# B4
	RD     = 0x20	# B5
	IORQ   = 0x40	# B6
	BUSACK = 0x80	# B7

	cpuControl = None
	# 0x0F - control, clock, etc
	BUSREQ = 0x01
	RESET  = 0x02
	CLKEN  = 0x04
	CLKOUT = 0x08
	# 0xF0 - unused

	cpuAddress = None
	# A0-A7, B0-B7 - Address lines (reversed)
	

	def bitReverse( data ):
		retval = 0
		if( (data & 0x80) == 0x80 ):	retval = retval | 0x01
		if( (data & 0x40) == 0x40 ):	retval = retval | 0x02
		if( (data & 0x20) == 0x20 ):	retval = retval | 0x04
		if( (data & 0x10) == 0x10 ):	retval = retval | 0x08
		if( (data & 0x08) == 0x08 ):	retval = retval | 0x10
		if( (data & 0x04) == 0x04 ):	retval = retval | 0x20
		if( (data & 0x02) == 0x02 ):	retval = retval | 0x40
		if( (data & 0x01) == 0x01 ):	retval = retval | 0x80

		return retval;

	addr = 0x20
x    def __init__(self, bus, addr, verbose):
        self.ixData = MCP23017(bus, addr+1)
        self.ixControl = PCF8574(bus, addr+2)
        self.ixAddress = MCP23017(bus, addr+3)


	##################################
	# Initialization
	
	def __init__( self, _ardy, _i2cAddr8 = None ):
		# set the arduino object
		self.ardy = _ardy
		self.cpuIoData  = MCP23017_IOExpander16( _ardy, 0x21 );
		self.cpuControl = PCF8574_IOExpander8( _ardy, 0x22 );
		self.cpuAddress = MCP23017_IOExpander16( _ardy, 0x23 );

	##################################
	# Low-level commands

	##################################
	# Package commands

	def SupervisorDelay( self ):
		delay( 1 )

	def Reset( self ):
		# RESET = 0
		self.SupervisorDelay()
		# RESET = 1
		return;

	def TakeBus( self ):
		BUSREQ = 0
		while True:
			data.get( GPIO[1] )
			if BUSAQ & 1 = 0
				break
		address[0] = iodir = 0 #output
		address[1] = iodir = 0 #output
		data.iodir |= M1, CLK, INT, BUSACK
		data, setgpio	MREQ WR RD IORQ
		set bank
		return

	def ReleaseBus( self ):
		address[0].iodir = 0xff # input (high-z)
		address[1].iodir = 0xff # input (high-z)
		data.iodir = 0xff
		if( reset ) supervisorDelay
		busreq = 1
		while trie
			get gpio[1]
			if busaq != 0
				break
		return

	def SlowClock( self ):
		period = 1.0/Float( rate )/2.0
		clken = 0
		while true:
			clkout = 0
			sleep( period )
			clkout = 1
			sleep( period )
		return

	def NormalClock( self ):
		CLKEN =1
		return
	
	def SetAddress( self, addr ):
		gpio0 = bitswap( addr >> 8 )
		gpio1 = bitswap( addr & 0xff )
		return

	##############################

	def MemRead( self, addr ):
		set address( addr)
		rd = 0
		mreq = 0
		result = daa.getgpio(0)
		rd = 1
		MREQ = 1
		return 0xff

	def MemWrite( self, addr, data ):
		set address( addr )
		data.setgpio( val )
		wr = 0
		mreq = 0
		wr = 1
		mreq = 1
		iodir0 = 0xff
		return

	def IORead( self, addr ):
		set address (addr )
		rd = 0
		iorq = 0
		val = data.getgpio
		rd = 1
		iorq = 1
		return 0xff

	def IOWrite( self, addr, data ):
		set address( addr )
		iodir 0 = 0x00
		data.setgpio( data )
		wr = 0
		iorq = 0
		wr = 1
		iorq = 1
		iodir 0 = 0xff
		return
