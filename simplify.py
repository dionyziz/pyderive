from math import *
from ast import *

class SimplificationException( Exception ):
    pass

def simplify( expr ):
    if isinstance( expr, astBooleanOperator ):
        expr.left = simplify( expr.left )
        expr.right = simplify( expr.right )
    if isinstance( expr, astVar ) or isinstance( expr, astConst ):
        return expr
    if isinstance( expr, astPlus ):
        if isinstance( expr.left, astConst ) and expr.left.const == 0:
            return expr.right
        if isinstance( expr.right, astConst ) and expr.right.const == 0:
            return expr.left
        if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
            return astConst( expr.left.const + expr.right.const )
        return expr
    if isinstance( expr, astMinus ):
        if isinstance( expr.left, astConst ) and expr.left.const == 0:
            return simplify( astUminus( expr.right ) )
        if isinstance( expr.right, astConst ) and expr.right.const == 0:
            return expr.left
        if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
            return astConst( expr.left.const - expr.right.const )
        return expr
    if isinstance( expr, astTimes ):
        if isinstance( expr.left, astConst ) and expr.left.const == 0:
            return astConst( 0 )
        if isinstance( expr.right, astConst ) and expr.right.const == 0:
            return astConst( 0 )
        if isinstance( expr.left, astConst ) and expr.left.const == 1:
            return expr.right
        if isinstance( expr.right, astConst ) and expr.right.const == 1:
            return expr.left
        if isinstance( expr.left, astConst ) and expr.left.const == -1:
            return simplify( astUminus( expr.right ) )
        if isinstance( expr.right, astConst ) and expr.right.const == -1:
            return simplify( astUminus( expr.left ) )
        if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
            return astConst( expr.left.const * expr.right.const )
        return expr
    if isinstance( expr, astUminus ):
        expr.arg = simplify( expr.arg )
        if isinstance( expr.arg, astConst ):
            return astConst( -expr.arg.const )
        return expr
    if isinstance( expr, astDivide ):
        if isinstance( expr.left, astConst ) and expr.left.const == 0:
            return astConst( 0 )
        if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
            if expr.right == 0:
                raise ZeroDivisionError 
            return astConst( expr.left.const / expr.right.const )
        return expr
    if isinstance( expr, astPower ):
        if isinstance( expr.right, astConst ) and expr.right.const == 1:
            return expr.left
        if isinstance( expr.right, astConst ) and expr.right.const < 0:
            return astDivide(
                astConst( 1 ),
                astPower( expr.left, astConst( -expr.right.const ) )
            )
        return expr
    if isinstance( expr, astFunc ):
        expr.arg = simplify( expr.arg )
        if isinstance( expr.arg, astConst ):
            return {
                'sin': lambda:
                    sin( expr.arg.const ),
                'cos': lambda:
                    cos( expr.arg.const ),
                'tan': lambda:
                    tan( expr.arg.const ),
                'exp': lambda:
                    exp( expr.arg.const ),
                'ln': lambda:
                    log( expr.arg.const )
            }[ expr.func ]()
        return expr
    raise SimplificationException
