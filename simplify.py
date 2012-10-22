from math import *
from ast import *

class SimplificationException( Exception ):
    pass

def decomposePolyonym( polyonym ):
    ret = []
    if isinstance( polyonym, astPlus ):
        return decomposePolyonym( polyonym.left ) + decomposePolyonym( polyonym.right )
    elif isinstance( polyonym, astMinus ):
        return decomposePolyonym( polyonym.left ) + decomposePolyonym( -polyonym.right )
    else:
        # it is a mononym
        if isinstance( polyonym, astUminus ):
            return [ ( '-', polyonym.arg ) ]
        else:
            return [ ( '+', polyonym ) ]

def composePolyonym( mononyms ):
    ( sign, expr ) = mononyms[ 0 ]
    if sign == '+':
        ret = expr
    else:
        ret = -expr
    for ( sign, expr ) in mononyms[ 1: ]:
        if sign == '+':
            ret += expr
        else:
            ret -= expr
    return ret

def unifyPolyonymMononyms( a, b ):
    """Take two mononyms of a polyonym and attempt to unify them.

    Return values can be:
    * None, if no unification is possible
    * A single astNode instance, if the two factors have been successfully unified
    * A list of astNodes if the unification yielded multiple terms (e.g. by expansion)
    """
    # minuses have been pulled out by the polyonym decomposer
    assert( not isinstance( a, astUminus ) )
    assert( not isinstance( b, astUminus ) )

    ( s, p ) = a
    ( t, q ) = b

    if isinstance( p, astConst ) and p.const == 0:
        return b
    if isinstance( q, astConst ) and q.const == 0:
        return a
    if isinstance( p, astConst ) and isinstance( q, astConst ):
        if s == t:
            return ( s, astConst( p.const + q.const ) )
        if p.const > q.const:
            return ( s, astConst( p.const - q.const ) )
        return ( t, astConst( q.const - p.const ) )
    if isinstance( p, astTimes ) and isinstance( p.left, astConst ) \
       and isinstance( q, astTimes ) and isinstance( q.left, astConst ) \
       and p.right == q.right:
        # n * a + m * a = (n + m) * a
        ( sign, factor ) = unifyPolyonymMononyms( ( s, p.left ), ( t, q.left ) )
        return ( sign, simplify( factor * p.right ) )
    if isinstance( p, astTimes ) and isinstance( p.left, astConst ) \
       and q == p.right:
        # n * a + 1 * a = (n + 1) * a
        return unifyPolyonymMononyms( a, ( t, astConst( 1 ) * q ) )
    if isinstance( q, astTimes ) and isinstance( q.left, astConst ) \
       and p == q.right:
        # 1 * a + n * a = (n + 1) * a
        return unifyPolyonymMononyms( ( s, astConst( 1 ) * p ), b )
    if p == q:
        # a + a = 2a
        return unifyPolyonymMononyms( ( s, astConst( 1 ) * p ), ( t, astConst( 1 ) * q ) )
    return None

def simplifyPolyonym( polyonym ):
    mononyms = decomposePolyonym( polyonym )
    # print( "Decomposed polyonym %s" % polyonym )
    # print( mononyms )
    unificationNeeded = True
    while unificationNeeded:
        # print( "Simplifying polyonym consisting of mononyms:" )
        # print( mononyms )
        unificationNeeded = False
        for i, parti in enumerate( mononyms ):
            for j, partj in enumerate( mononyms[ i + 1: ] ):
                res = unifyPolyonymMononyms( parti, partj )
                if res is not None:
                    unificationNeeded = True
                    # print( "Unified mononyms: " )
                    # print( parti )
                    # print( partj )
                    # print( " = %s %s" % res )
                    # print( 'At locations %i and %i' % ( i, j ) )
                    # found a possible unification between two terms of the polyonym
                    del mononyms[ j + i + 1 ]
                    del mononyms[ i ]
                    # discard terms unified to 0
                    if res[ 1 ] != astConst( 0 ):
                        mononyms.append( res )
                    break
            if unificationNeeded:
                break
    mononyms.sort()
    if len( mononyms ) == 0:
        # unification may have cancelled everything out
        return astConst( 0 )
    return composePolyonym( mononyms )

def simplifyPlus( expr ):
    return simplifyPolyonym( expr )

def simplifyMinus( expr ):
    return simplifyPolyonym( expr )

def expand( multiplication ):
    assert( isinstance( multiplication, astTimes ) )

    # apply distributivity law
    factorTerms = decomposePolyonym( multiplication.left )
    exprTerms = decomposePolyonym( multiplication.right )
    ret = []
    for ( signA, a ) in factorTerms:
        for ( signB, b ) in exprTerms:
            if signA == signB:
                ret.append( ( '+', a * b ) )
            else:
                ret.append( ( '-', a * b ) )
    return simplify( composePolyonym( ret ) )

def decomposeMononym( mononym ):
    """Take a mononym and break it into factoring parts. Extract the sign.
    
    e.g. 2 * x * y is broken down to ( +, [ 2, x, y ] )
    """

    if isinstance( mononym, astTimes ):
        ( signleft, left ) = decomposeMononym( mononym.left )
        ( signright, right ) = decomposeMononym( mononym.right )
        if signleft == signright:
            return ( '+', left + right )
        return ( '-', left + right )
    if isinstance( mononym, astUminus ):
        return ( '-', [ mononym ] )
    if isinstance( mononym, astConst ) and mononym.const < 0:
        return ( '-', [ mononym ] )
    return ( '+', [ mononym ] )

def composeMononym( terms ):
    if len( terms ) == 1:
        return terms[ 0 ]
    # compose it into the form
    # a * (b * (c * ... ))
    # that way the constant factors are up in the front
    # and can be manipulated easily by the polyonym simplifier
    return terms[ 0 ] * composeMononym( terms[ 1: ] )

def unifyMononymFactors( a, b ):
    """Take two factors of a mononym and attempt to unify them.

    Return values can be:
    * None, if no unification is possible
    * A single astNode instance, if the two factors have been successfully unified
    * A list of astNodes if the unification yielded multiple terms (e.g. by expansion)
    """

    # uminuses have been simplified during mononym decomposition
    assert( not isinstance( a, astUminus ) )
    assert( not isinstance( b, astUminus ) )

    if isinstance( a, astConst ) and isinstance( b, astConst ):
        return astConst( a.const * b.const )
    if isinstance( a, astConst ):
        if a.const == 0:
            return a
        if a.const == 1:
            return b
    if isinstance( b, astConst ):
        if b.const == 0:
            return b
        if b.const == 1:
            return a
        # the -1 case is handled by pulling out the - in front of the -1 constant
        # and leaving a constant of 1 to be unified at this point
    if isinstance( a, astPlus ) or isinstance( b, astPlus ) \
    or isinstance( a, astMinus ) or isinstance( b, astMinus ):
        # print( "Expanding %s times %s" % ( a, b ) )
        expanded = expand( a * b )
        # print( "into %s" % expanded )
        return expanded
    if isinstance( a, astVar ) and isinstance( b, astVar ):
        if a.var == b.var:
            return a ** astConst( 2 )

    # x^n * x^m = x^(n + m)
    if isinstance( a, astPower ) and isinstance( b, astPower ) \
       and isinstance( a.left, astVar ) and isinstance( b.left, astVar ) \
       and isinstance( a.right, astConst ) and isinstance( b.right, astConst ) \
       and a.left.var == b.left.var:
        return a.left ** ( a.right + b.right )
    # x * x^n = x^( n + 1 )
    if isinstance( a, astPower ) and isinstance( b, astVar ) \
       and isinstance( a.left, astVar ) and a.left.var == b.var:
       return unifyMononymFactors( a, b ** astConst( 1 ) )
    # x^n * x = x^( n + 1 )
    if isinstance( b, astPower ) and isinstance( a, astVar ) \
       and isinstance( b.left, astVar ) and b.left.var == a.var:
       return unifyMononymFactors( b ** astConst( 1 ), a )
    return None
    
def simplifyMononym( mononym ):
    ( sign, parts ) = decomposeMononym( mononym )
    unificationNeeded = True
    while unificationNeeded:
        unificationNeeded = False
        for i, parti in enumerate( parts ):
            for j, partj in enumerate( parts[ i + 1: ] ):
                res = unifyMononymFactors( parti, partj )
                if res is not None:
                    # we found a possible unification between two factors
                    # parti and partj
                    # combine them, remove the original parts and
                    # restart unification from scratch
                    unificationNeeded = True
                    del parts[ j + i + 1 ]
                    del parts[ i ]
                    if isinstance( res, astNode ):
                        parts.append( res )
                    else:
                        # parts is a list
                        parts += res
                    break
            if unificationNeeded:
                break
    parts.sort()
    return composeMononym( parts )

def simplifyTimes( expr ):
    return simplifyMononym( expr )

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
    if isinstance( expr.left, astConst ) and isinstance( expr.right, astConst ):
        return astConst( expr.left.const ** expr.right.const )
    if isinstance( expr.right, astConst ) and expr.right.const == 1:
        return expr.left
    if isinstance( expr.right, astConst ) and expr.right.const < 0:
        return astConst( 1 ) / ( expr.left ** astConst( -expr.right.const ) )
    if isinstance( expr.left, astPower ) \
       and isinstance( expt.left.right, astConst ) \
       and isinstance( expr.right, astConst ):
        # ( a^n )^m = a^(n*m)
        return expr.left.left ** simplify( expr.left.right * expr.right )
    if isinstance( expr.left, astTimes ):
        # expand exponential
        return simplify( expr.left.left ** expr.right ) * simplify( expr.left.right ** expr.right )
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

# print(
#     simplify(
#         astTimes(
#             astConst( 3 ) * ( astVar( 'x' ) ** astConst( 2 ) ) + astConst( 4 ) * astVar( 'x' ) + astConst( 9 ),
#             astVar( 'x' ) ** astConst( 3 ) + astVar( 'x' )
#         )
#     )
# )

# print( decomposeMononym( astConst( 2 ) * ( astVar( 'x' ) ** astConst( 2 ) ) * astFunc( 'sin', astVar( 'x' )  ) ) )
# Testcase: x + y + z + 2 * y + 2 * x - x
