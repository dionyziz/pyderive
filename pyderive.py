import parser
from derive import *

while 1:
    try:
        s = raw_input( 'pyderive > ' )
    except EOFError:
        break
    # print( parser.parse( s ) )
    print( derive( parser.parse( s ), 'x' ) )
