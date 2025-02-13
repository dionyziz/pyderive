from ast import *


class DerivationException(Exception):
    pass


def deriveFunc(func, argument, withRespectTo):
    return {
        "sin": lambda: astFunc("cos", argument),
        "cos": lambda: -astFunc("sin", argument),
        "tan": lambda: derive(
            astFunc("sin", argument) / astFunc("cos", argument), withRespectTo
        ),
        "exp": lambda: astFunc("exp", argument),
        "ln": lambda: astConst(1) / argument,
    }[func]()


def deriveVar(expr, withRespectTo):
    if expr.var == withRespectTo:
        return astConst(1)
    return astConst(0)


def derive(expr, withRespectTo):
    if isinstance(expr, astVar):
        return deriveVar(expr, withRespectTo)
    if isinstance(expr, astConst):
        return astConst(0)
    if isinstance(expr, astPlus):
        # derivative of a sum is the sum of the derivatives
        return derive(expr.left, withRespectTo) + derive(expr.right, withRespectTo)
    if isinstance(expr, astMinus):
        return derive(expr.left, withRespectTo) - derive(expr.right, withRespectTo)
    if isinstance(expr, astUminus):
        return -derive(expr.arg, withRespectTo)
    if isinstance(expr, astTimes):
        # product rule
        return derive(expr.left, withRespectTo) * expr.right + expr.left * derive(
            expr.right, withRespectTo
        )
    if isinstance(expr, astDivide):
        return (
            derive(expr.left, withRespectTo) * expr.right
            - expr.left * derive(expr.right, withRespectTo)
        ) / (expr.right ** astConst(2))
    if isinstance(expr, astPower):
        if isinstance(expr.right, astConst):
            return (
                expr.right
                * (expr.left ** astConst(expr.right.const - 1))
                * derive(expr.left, withRespectTo)
            )
        return derive(
            astFunc("exp", expr.right * astFunc("ln", expr.left)), withRespectTo
        )
    if isinstance(expr, astFunc):
        # chain rule
        return derive(expr.arg, withRespectTo) * deriveFunc(
            expr.func, expr.arg, withRespectTo
        )
    raise DerivationException()
