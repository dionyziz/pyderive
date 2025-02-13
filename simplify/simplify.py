from math import *
from ast import *
from .monomial import *
from .polynomial import *


class SimplificationException(Exception):
    pass


def simplifyPlus(expr):
    return simplifyPolynomial(expr)


def simplifyMinus(expr):
    return simplifyPolynomial(expr)


def expand(multiplication):
    assert isinstance(multiplication, astTimes)

    # apply distributivity law
    factorTerms = decomposePolynomial(multiplication.left)
    exprTerms = decomposePolynomial(multiplication.right)
    ret = []
    for signA, a in factorTerms:
        for signB, b in exprTerms:
            if signA == signB:
                ret.append((PLUS, a * b))
            else:
                ret.append((MINUS, a * b))
    return simplify(composePolynomial(ret))


def simplifyTimes(expr):
    return simplifyMonomial(expr)


def simplifyUminus(expr):
    expr.arg = simplify(expr.arg)
    if isinstance(expr.arg, astConst):
        return astConst(-expr.arg.const)
    if isinstance(expr.arg, astUminus):
        return expr.arg.arg
    # if isinstance( expr.arg, astTimes ) \
    #    and isinstance( expr.arg.left, astConst ):
    #     # pull the uminus into the monomial constant
    #     return ( -expr.arg.left ) * expr.arg.right
    if isinstance(expr.arg, astPlus) or isinstance(expr.arg, astMinus):
        # uminus expansion
        return simplifyPolynomial(
            composePolynomial(
                [(not sign, expr) for (sign, expr) in decomposePolynomial(expr.arg)]
            )
        )
    return expr


def simplifyDivide(expr):
    if isinstance(expr.left, astConst) and expr.left.const == 0:
        return astConst(0)
    if isinstance(expr.left, astConst) and isinstance(expr.right, astConst):
        if expr.right == 0:
            raise ZeroDivisionError
        return astConst(expr.left.const / expr.right.const)
    return expr


def simplifyPower(expr):
    if isinstance(expr.left, astConst) and isinstance(expr.right, astConst):
        return astConst(expr.left.const**expr.right.const)
    if isinstance(expr.right, astConst) and expr.right.const == 1:
        return expr.left
    if isinstance(expr.right, astConst) and expr.right.const < 0:
        return astConst(1) / (expr.left ** astConst(-expr.right.const))
    if (
        isinstance(expr.left, astUminus)
        and isinstance(expr.right, astConst)
        and expr.right.const % 2 == 0
    ):
        # even powers cancel negative signs
        return expr.left.arg**expr.right
    if (
        isinstance(expr.left, astPlus)
        and isinstance(expr.right, astConst)
        and expr.right.const == 2
    ):
        # ( a + b )^2 = a^2 + 2ab + b^2
        a = expr.left.left
        b = expr.left.right
        # we need to simplify again as, for instance, "b"
        # could be a sum of its own
        s = a ** astConst(2) + astConst(2) * a * b + b ** astConst(2)
        return simplify(s)
    if (
        isinstance(expr.left, astMinus)
        and isinstance(expr.right, astConst)
        and expr.right.const == 2
    ):
        # ( a - b )^2 = a^2 - 2ab + b^2
        a = expr.left.left
        b = expr.left.right
        return simplify((a ** astConst(2)) - (astConst(2) * a * b) + (b ** astConst(2)))
    if (
        isinstance(expr.left, astPower)
        and isinstance(expt.left.right, astConst)
        and isinstance(expr.right, astConst)
    ):
        # ( a^n )^m = a^(n*m)
        return expr.left.left ** simplify(expr.left.right * expr.right)
    if isinstance(expr.left, astTimes):
        # expand exponential
        return simplify(expr.left.left**expr.right) * simplify(
            expr.left.right**expr.right
        )
    return expr


def simplifyFunc(expr):
    expr.arg = simplify(expr.arg)
    if isinstance(expr.arg, astConst):
        return {
            "sin": lambda: sin(expr.arg.const),
            "cos": lambda: cos(expr.arg.const),
            "tan": lambda: tan(expr.arg.const),
            "exp": lambda: exp(expr.arg.const),
            "ln": lambda: log(expr.arg.const),
        }[expr.func]()
    return expr


def simplify(expr):
    if isinstance(expr, astBooleanOperator):
        expr.left = simplify(expr.left)
        expr.right = simplify(expr.right)
    if isinstance(expr, astVar) or isinstance(expr, astConst):
        return expr
    if isinstance(expr, astPlus):
        return simplifyPlus(expr)
    if isinstance(expr, astMinus):
        return simplifyMinus(expr)
    if isinstance(expr, astTimes):
        return simplifyTimes(expr)
    if isinstance(expr, astUminus):
        return simplifyUminus(expr)
    if isinstance(expr, astDivide):
        return simplifyDivide(expr)
    if isinstance(expr, astPower):
        return simplifyPower(expr)
    if isinstance(expr, astFunc):
        return simplifyFunc(expr)
    return expr


# print(
#     simplify(
#         astTimes(
#             astConst( 3 ) * ( astVar( 'x' ) ** astConst( 2 ) ) + astConst( 4 ) * astVar( 'x' ) + astConst( 9 ),
#             astVar( 'x' ) ** astConst( 3 ) + astVar( 'x' )
#         )
#     )
# )

# print( decomposeMonomial( astConst( 2 ) * ( astVar( 'x' ) ** astConst( 2 ) ) * astFunc( 'sin', astVar( 'x' )  ) ) )
