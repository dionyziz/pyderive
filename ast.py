from math import *

class AbstractClassException( Exception ):
    pass

class astNode( object ):
    def __init__( self ):
        raise AbstractClassException
    def __repr__( self ):
        return self.toString( 1 )
    def __ne__( self, y ):
        return not self == y

class astVar( astNode ):
    def __init__( self, var ):
        self.var = var
    def toString( self, level ):
        return self.var
    def __eq__( self, y ):
        return self.var == y.var

class astConst( astNode ):
    def __init__( self, const ):
        self.const = float( const )
    def toString( self, level ):
        if self.const.is_integer():
            return str( int( self.const ) )
        return str( self.const )
    def __eq__( self, y ):
        return self.const == y.const

class astBooleanOperator( astNode ):
    def toString( self, level ):
        return parenthesize(
            self.left.toString( self.priority )
          + ' ' + self.operator + ' '
          + self.right.toString( self.priority ),
            self.priority,
            level
        )
    def __init__( self, left, right ):
        self.left = left
        self.right = right
    def __eq__( self, y ):
        return self.__class__.__name__ == y.__class__.__name__ \
           and self.left == y.left \
           and self.right == y.right

class astPlus( astBooleanOperator ):
    operator = '+'
    priority = 1

class astMinus( astBooleanOperator ):
    operator = '-'
    priority = 1

class astTimes( astBooleanOperator ):
    operator = '*'
    priority = 2

class astDivide( astBooleanOperator ):
    operator = '/'
    priority = 2

class astPower( astBooleanOperator ):
    operator = '^'
    priority = 3

class astUminus( astNode ):
    priority = 4
    def toString( self, level ):
        return parenthesize(
            '-' + self.arg.toString( 4 ),
            self.priority,
            level
        )
    def __init__( self, arg ):
        self.arg = arg
    def __eq__( self, y ):
        return self.arg == y.arg

class astFunc( astNode ):
    def toString( self, level ):
        return self.func + '(' + self.arg.toString( 1 ) + ')'
    def __init__( self, func, arg ):
        self.func = func
        self.arg = arg
    def __eq__( self, y ):
        return self.func == y.func \
           and self.arg == y.arg

def parenthesize( expression, selfLevel, parentLevel ):
    if selfLevel < parentLevel:
        left, right = '(', ')'
    else:
        left, right = '', ''
    return left + expression + right
