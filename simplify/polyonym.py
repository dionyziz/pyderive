from ast import *
import simplify

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
        return ( sign, simplify.simplify( factor * p.right ) )
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

