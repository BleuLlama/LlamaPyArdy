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

	# our mirror values here
	data = 0
	dataControl = 0
	dataAddress = 0
	
    ##############################	
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

		return retval

	##################################
	# Initialization
	
	def __init__( self, _ardy, _i2cAddr8 = None ):
		# set the arduino object
		baseAddr = _i2cAddr8
		if _i2cAddr8 is None:
			baseAddr = 0x21

		self.data = 0
		self.dataControl = 0
		self.dataAddress = 0

		self.ardy = _ardy
		self.cpuIoData  = MCP23017_IOExpander16( _ardy, baseAddr + 0 )
		self.cpuControl = PCF8574_IOExpander8( _ardy, baseAddr + 1 )
		self.cpuAddress = MCP23017_IOExpander16( _ardy, baseAddr + 2 )

		self.ClearAllExpanders()

	def ClearAllExpaners( self ):
		# clear data register
		self.cpuIoData.DirectionA( IODIRA, IOALLINPUT )
		self.cpuIoData.SetA( 0x00 )
		self.cpuIoData.DirectionB( IODIRA, IOALLINPUT )
		self.cpuIoData.SetB( 0x00 )

		# clear control register
		self.cpuControl.Set( 0x00 )

		# clear address register
		self.cpuAddress.DirectionA( IOALLINPUT )
		self.cpuAddress.SetA( 0x00 )
		self.cpuAddress.DirectionB( IOALLINPUT )
		self.cpuAddress.SetB( 0x00 )

	##################################
	# Low-level commands

	##################################
	# Package commands

	def SupervisorDelay( self ):
		delay( 1 )

	def Reset( self ):
		# RESET = 0
		value = 0x00
		self.cpuControl.Set( value )
		self.SupervisorDelay()

		# RESET = 1
		value = self.RESET
		self.cpuControl.Set( value )
		return

	def TakeBus( self ):
		value = self.BUSREQ
		self.cpuControl.Set( value )

		while True:
			value = self.cpuIoData.GetB( )
			if (value & BUSAQ) == 0
				break

		self.cpuAddress.DirectionA( IOALLINPUT )
		self.cpuAddress.DirectionB( IOALLINPUT )

		value = M1 | C
		data.iodir |= M1, CLK, INT, BUSACK
		data, setgpio	MREQ WR RD IORQ
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
