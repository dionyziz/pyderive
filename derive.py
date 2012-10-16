from ast import *

class DerivationException( Exception ):
    pass

def deriveFunc( func, argument, withRespectTo ):
    return {
        'sin': lambda:
            astFunc( 'cos', argument ),
        'cos': lambda:
            astUminus( astFunc( 'sin', argument ) ),
        'tan': lambda:
            derive(
                astDivide(
                    astFunc( 'sin', argument ),
                    astFunc( 'cos', argument )
                ),
                withRespectTo
            ),
        'exp': lambda:
            astFunc( 'exp', argument ),
        'ln': lambda:
            astDivide(
                astConst( 1 ),
                argument
            )
    }[ func ]()

def deriveVar( expr, withRespectTo ):
    if expr.var == withRespectTo:
        return astConst( 1 )
    return astConst( 0 )

def derive( expr, withRespectTo ):
    if isinstance( expr, astVar ):
        return deriveVar( expr, withRespectTo )
    if isinstance( expr, astConst ):
        return astConst( 0 )
    if isinstance( expr, astPlus ):
        return astPlus( derive( expr.left, withRespectTo ), derive( expr.right, withRespectTo ) )
    if isinstance( expr, astMinus ):
        return astMinus( derive( expr.left, withRespectTo ), derive( expr.right, withRespectTo ) )
    if isinstance( expr, astTimes ):
        return astPlus(
            astTimes( derive( expr.left, withRespectTo ), expr.right ),
            astTimes( expr.left, derive( expr.right, withRespectTo ) )
        )
    if isinstance( expr, astUminus ):
        return astUminus( derive( expr.left, withRespectTo ) )
    if isinstance( expr, astDivide ):
        return astDivide(
            astMinus(
                astTimes( derive( expr.left, withRespectTo ), expr.right ),
                astTimes( expr.left, derive( expr.right, withRespectTo ) )
            ),
            astPower(
                expr.right,
                astConst( 2 )
            )
        )
    if isinstance( expr, astPower ):
        if isinstance( expr.right, astConst ):
            return astTimes(
                expr.right,
                astTimes(
                    astPower(
                        expr.left, astConst( expr.right.const - 1 )
                    ),
                    derive( expr.left, withRespectTo )
                )
            )
        return derive( astFunc(
            'exp',
            astTimes(
                expr.right,
                astFunc(
                    'ln',
                    expr.left
                )
            )
        ), withRespectTo )
    if isinstance( expr, astFunc ):
        # chain rule
        return astTimes(
            derive( expr.arg, withRespectTo ),
            deriveFunc( expr.func, expr.arg, withRespectTo )
        )
    raise DerivationException()
