from parser import *
from derive import *
from simplify import *
from help import *

print( 'PyDerive - A symbolic derivation tool.' )
print( 'Type `help` for help.' )

mode = 'derive'
modes = [ 'derive', 'simplify', 'derive-only', 'parse' ]
var = 'x'

while 1:
    try:
        s = raw_input( 'pyderive > ' )
    except EOFError:
        print( '\nGoodbye' )
        break
    args = s.split( ' ' )
    command = args[ 0 ]
    # print( simplify( parse( s ) ) )
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
        except ParseException:
            print( 'Syntax error' )
