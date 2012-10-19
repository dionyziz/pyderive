from math import *
from ast import *

class SimplificationException( Exception ):
    pass

def decomposePolyonym( polyonym ):
    pass

def composePolyonym( mononyms ):
    ( sign, expr ) = mononyms[ 0 ]
    if sign == '+':
        ret = mononym
    else:
        ret = -mononym
    for ( sign, expr ) in mononyms:
        if sign == '+':
            ret += expr
        else:
            ret -= expr
    return ret

def simplifyPlus( expr ):
    if isinstance( expr.left, astConst ) and expr.left.const == 0:
        return expr.right
    if isinstance( expr.right, astConst ) and expr.right.const == 0:
        return expr.left
    if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
        return astConst( expr.left.const + expr.right.const )
    if isinstance( expr.right, astUminus ):
        return simplify( expr.left + expr.right.arg )
    if isinstance( expr.left, astUminus ):
        return simplify( expr.right - expr.left.arg )
    return expr

def simplifyMinus( expr ):
    if isinstance( expr.left, astConst ) and expr.left.const == 0:
        return simplify( -expr.right )
    if isinstance( expr.right, astConst ) and expr.right.const == 0:
        return expr.left
    if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
        return astConst( expr.left.const - expr.right.const )
    if isinstance( expr.right, astUminus ):
        return simplify( expr.left + expr.right.arg )
    return expr

def simplifyTimes( expr ):
    if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
        return astConst( expr.left.const * expr.right.const )
    if isinstance( expr.right, astConst ):
        # put constant factor on the left
        return simplify( expr.right * expr.left )
    if isinstance( expr.left, astUminus ):
        # pull out the minus
        return simplify( expr.left.arg * expr.right )
    if isinstance( expr.right, astUminus ):
        return simplify( expr.left * expr.right.arg ) 
    if isinstance( expr.left, astConst ):
        if expr.left.const == 0:
            return astConst( 0 )
        if expr.left.const == 1:
            return expr.right
        if expr.left.const == -1:
            return simplify( -expr.right )
    return expr

def simplifyUminus( expr ):
    expr.arg = simplify( expr.arg )
    if isinstance( expr.arg, astConst ):
        return astConst( -expr.arg.const )
    return expr

def simplifyDivide( expr ):
    if isinstance( expr.left, astConst ) and expr.left.const == 0:
        return astConst( 0 )
    if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
        if expr.right == 0:
            raise ZeroDivisionError 
        return astConst( expr.left.const / expr.right.const )
    return expr

def simplifyPower( expr ):
    if isinstance( expr.right, astConst ) and expr.right.const == 1:
        return expr.left
    if isinstance( expr.right, astConst ) and expr.right.const < 0:
        return astConst( 1 ) / ( expr.left ** astConst( -expr.right.const ) )
    return expr

def simplifyFunc( expr ):
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

def simplify( expr ):
    if isinstance( expr, astBooleanOperator ):
        expr.left = simplify( expr.left )
        expr.right = simplify( expr.right )
    if isinstance( expr, astVar ) or isinstance( expr, astConst ):
        return expr
    if isinstance( expr, astPlus ):
        return simplifyPlus( expr )
    if isinstance( expr, astMinus ):
        return simplifyMinus( expr )
    if isinstance( expr, astTimes ):
        return simplifyTimes( expr )
    if isinstance( expr, astUminus ):
        return simplifyUminus( expr )
    if isinstance( expr, astDivide ):
        return simplifyDivide( expr )
    if isinstance( expr, astPower ):
        return simplifyPower( expr )
    if isinstance( expr, astFunc ):
        return simplifyFunc( expr )
    return expr
