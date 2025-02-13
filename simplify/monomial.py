from ast import *
from . import simplify

def decomposeMonomial( monomial ):
    """Take a monomial and break it into factoring parts. Extract the sign.
    
    e.g. 2 * x * y is broken down to ( +, [ 2, x, y ] )
    """

    if isinstance( monomial, astTimes ):
        ( signleft, left ) = decomposeMonomial( monomial.left )
        ( signright, right ) = decomposeMonomial( monomial.right )
        if signleft == signright:
            return ( PLUS, left + right )
        return ( MINUS, left + right )
    if isinstance( monomial, astUminus ):
        return ( MINUS, [ monomial.arg ] )
    if isinstance( monomial, astConst ):
        if monomial.const == -1:
            return ( MINUS, [] )
        if monomial.const == 1:
            return ( PLUS, [] )
        if monomial.const < 0:
            return ( MINUS, [ astConst( -monomial.const ) ] )
    return ( PLUS, [ monomial ] )

def composeMonomial( terms ):
    if len( terms ) == 0:
        # monomial of no terms
        return astConst( 1 )
    if len( terms ) == 1:
        return terms[ 0 ]
    # compose it into the form
    # a * (b * (c * ... ))
    # that way the constant factors are up in the front
    # and can be manipulated easily by the polynomial simplifier
    return terms[ 0 ] * composeMonomial( terms[ 1: ] )

def unifyMonomialFactors( a, b ):
    """Take two factors of a monomial and attempt to unify them.

    Return values can be:
    * None, if no unification is possible
    * A single astNode instance, if the two factors have been successfully unified
    * A list of astNodes if the unification yielded multiple terms (e.g. by expansion)
    """

    # uminuses have been simplified during monomial decomposition
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
        expanded = simplify.expand( a * b )
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
       return unifyMonomialFactors( a, b ** astConst( 1 ) )
    # x^n * x = x^( n + 1 )
    if isinstance( b, astPower ) and isinstance( a, astVar ) \
       and isinstance( b.left, astVar ) and b.left.var == a.var:
       return unifyMonomialFactors( b ** astConst( 1 ), a )
    return None
    
def simplifyMonomial( monomial ):
    ( sign, parts ) = decomposeMonomial( monomial )
    # print( "Decomposed monomial %s into:" % monomial )
    # print( sign )
    # print( parts )
    unificationNeeded = True
    while unificationNeeded:
        unificationNeeded = False
        for i, parti in enumerate( parts ):
            for j, partj in enumerate( parts[ i + 1: ] ):
                res = unifyMonomialFactors( parti, partj )
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
    expr = composeMonomial( parts )
    if sign == MINUS:
        res = astUminus( expr )
    else:
        res = expr
    if monomial != res:
        # may need to re-apply simplification
        # until we reach a fixed point
        # if, for example, the monomial simplification
        # yielded a polynomial through distributivity of multiplication
        return simplify.simplify( res )
    # we've reached a fixes point
    return res
