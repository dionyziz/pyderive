from parser import parse
from derive import *
from simplify import *

while 1:
    try:
        s = raw_input( 'pyderive > ' )
    except EOFError:
        break
    # print( simplify( parse( s ) ) )
    print( simplify( derive( parse( s ), 'x' ) ) )
