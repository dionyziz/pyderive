from ast import *
import simplify

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
        return ( '-', [ mononym.arg ] )
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
    expr = composeMononym( parts )
    if sign == '-':
        return astUminus( expr )
    return expr
