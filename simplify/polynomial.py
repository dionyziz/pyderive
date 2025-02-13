from ast import *
from . import simplify


def decomposePolynomial(polynomial):
    ret = []
    if isinstance(polynomial, astPlus):
        return decomposePolynomial(polynomial.left) + decomposePolynomial(
            polynomial.right
        )
    elif isinstance(polynomial, astMinus):
        if isinstance(polynomial.right, astUminus):
            return decomposePolynomial(polynomial.left) + decomposePolynomial(
                polynomial.right.arg
            )
        return decomposePolynomial(polynomial.left) + decomposePolynomial(
            simplify.simplify(-polynomial.right)
        )
    else:
        # it is a monomial
        if isinstance(polynomial, astUminus):
            return [(MINUS, polynomial.arg)]
        else:
            return [(PLUS, polynomial)]


def composePolynomial(monomials):
    (sign, expr) = monomials[0]
    if sign == PLUS:
        ret = expr
    else:
        ret = -expr
    for sign, expr in monomials[1:]:
        if sign == PLUS:
            ret += expr
        else:
            ret -= expr
    return ret


def unifyPolynomialMonomials(a, b):
    """Take two monomials of a polynomial and attempt to unify them.

    Return values can be:
    * None, if no unification is possible
    * A single astNode instance, if the two factors have been successfully unified
    * A list of astNodes if the unification yielded multiple terms (e.g. by expansion)
    """
    # minuses have been pulled out by the polynomial decomposer
    assert not isinstance(a, astUminus)
    assert not isinstance(b, astUminus)

    (s, p) = a
    (t, q) = b

    if isinstance(p, astConst) and p.const == 0:
        return b
    if isinstance(q, astConst) and q.const == 0:
        return a
    if isinstance(p, astConst) and isinstance(q, astConst):
        if s == t:
            return (s, astConst(p.const + q.const))
        if p.const > q.const:
            return (s, astConst(p.const - q.const))
        return (t, astConst(q.const - p.const))
    if (
        isinstance(p, astTimes)
        and isinstance(p.left, astConst)
        and isinstance(q, astTimes)
        and isinstance(q.left, astConst)
        and p.right == q.right
    ):
        # n * a + m * a = (n + m) * a
        (sign, factor) = unifyPolynomialMonomials((s, p.left), (t, q.left))
        return (sign, simplify.simplify(factor * p.right))
    if isinstance(p, astTimes) and isinstance(p.left, astConst) and q == p.right:
        # n * a + 1 * a = (n + 1) * a
        return unifyPolynomialMonomials(a, (t, astConst(1) * q))
    if isinstance(q, astTimes) and isinstance(q.left, astConst) and p == q.right:
        # 1 * a + n * a = (n + 1) * a
        return unifyPolynomialMonomials((s, astConst(1) * p), b)
    if p == q:
        # a + a = 2a
        return unifyPolynomialMonomials((s, astConst(1) * p), (t, astConst(1) * q))
    return None


def simplifyPolynomial(polynomial):
    monomials = decomposePolynomial(polynomial)
    # print( monomials )
    # print( "Decomposed polynomial %s" % polynomial )
    # print( monomials )
    unificationNeeded = True
    while unificationNeeded:
        # print( "Simplifying polynomial consisting of monomials:" )
        # print( monomials )
        unificationNeeded = False
        for i, parti in enumerate(monomials):
            for j, partj in enumerate(monomials[i + 1 :]):
                res = unifyPolynomialMonomials(parti, partj)
                if res is not None:
                    unificationNeeded = True
                    # print( "Unified monomials: " )
                    # print( parti )
                    # print( partj )
                    # print( " = %s %s" % res )
                    # print( 'At locations %i and %i' % ( i, j ) )
                    # found a possible unification between two terms of the polynomial
                    del monomials[j + i + 1]
                    del monomials[i]
                    # discard terms unified to 0
                    if res[1] != astConst(0):
                        monomials.append(res)
                    break
            if unificationNeeded:
                break
    monomials.sort()
    if len(monomials) == 0:
        # unification may have cancelled everything out
        return astConst(0)
    return composePolynomial(monomials)
