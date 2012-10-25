from parser import *
from derive import *
from simplify.simplify import simplify
import sys
from help import *

print( 'PyDerive - A symbolic derivation tool.' )
print( 'Type `help` for help.' )

mode = 'derive'
modes = [ 'derive', 'simplify', 'derive-only', 'parse' ]
var = 'x'

while 1:
    try:
        if mode == 'derive':
            if var == 'x':
                s = raw_input( '> ' )
            else:
                s = raw_input( 'd/d' + var + ' > ' )
        elif mode == 'simplify':
            s = raw_input( 'simplify > ' )
        elif mode == 'parse':
            s = raw_input( 'parse > ' )
        elif mode == 'derive-only':
            s = raw_input( 'derive-only > ' )
    except EOFError:
        print( '\nGoodbye' )
        break
    if len( s ) == 0:
        continue
    args = s.split( ' ' )
    command = args[ 0 ]
    if command == 'help':
        help( args )
    elif command == 'exit':
        print( 'Goodbye' )
        break
    elif command == 'diff':
        if len( args ) > 1:
            if len( args[ 1 ] ) != 1 or not 'a' <= args[ 1 ] <= 'z':
                help( [ 'diff' ] )
            var = args[ 1 ]
            print( 'Now differentiating with respect to variable %s.' % var )
        else:
            help( [ 'diff' ] )
    elif command == 'mode':
        if len( args ) > 1:
            if not args[ 1 ] in modes:
                help( [ 'modes' ] )
            else:
                mode = args[ 1 ]
                print( 'Mode of operation is now "%s".' % mode )
        else:
            # typing `mode` reverts to default mode
            mode = 'derive'
            print( 'Mode of operation is now "%s".' % mode )
    else:
        try:
            if mode == 'derive':
                res = simplify( derive( parse( s ), var ) )
            elif mode == 'simplify':
                res = simplify( parse( s ) )
            elif mode == 'parse':
                res = parse( s )
            elif mode == 'derive-only':
                res = derive( parse( s ), var )
            print( res )
        except LexException as e:
            print( 'Syntax error: Invalid character "%s"' % e.character )
        except ParseException:
            print( 'Syntax error' )
