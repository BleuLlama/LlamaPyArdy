
import array

class LlamaGamma:
    
    gammatable = array.array('i',(0,)*256)

    def __init__( self ):
	for i in range( 0, 256 ):
	    x = float( i )
	    x = x /255
	    x = pow( x, 2.5 )
	    x = x * 255
	    self.gammatable[i] = int( x )

    def adjust( self, raw ):
	value = int( raw )
	if value < 0:
	    value = 0

	if value > 255:
	    value = 255

	return self.gammatable[ value ]

    def dump( self ):
	for i in range( 0, 256 ):
	    print "{}: {}".format( i, self.adjust( i ))
