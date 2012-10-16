from ast import *

def deriveFunc( func, argument, withRespectTo ):
    return {
        'sin': lambda:
            astNode( AST_TYPE_FUNC, 'cos', argument ),
        'cos': lambda:
            astNode( AST_TYPE_UMINUS, astNode( AST_TYPE_FUNC, 'sin', argument ) ),
        'tan': lambda:
            derive(
                astNode( AST_TYPE_DIVIDE,
                    astNode( AST_TYPE_FUNC, 'sin', argument ),
                    astNode( AST_TYPE_FUNC, 'cos', argumetn )
                ),
                withRespectTo
            )
    }[ func ]()

def deriveVar( expr, withRespectTo ):
    if expr.left == withRespectTo:
        return astNode( AST_TYPE_CONST, 1 )
    return astNode( AST_TYPE_CONST, 0 )

def derive( expr, withRespectTo ):
    return {
        AST_TYPE_VAR: lambda:
            deriveVar( expr, withRespectTo ),
        AST_TYPE_CONST: lambda:
            astNode( AST_TYPE_CONST, 0 ),
        AST_TYPE_PLUS: lambda:
            astNode( AST_TYPE_PLUS, derive( expr.left, withRespectTo ), derive( expr.right, withRespectTo ) ),
        AST_TYPE_MINUS: lambda:
            astNode( AST_TYPE_MINUS, derive( expr.left, withRespectTo ), derive( expr.right, withRespectTo ) ),
        AST_TYPE_TIMES: lambda:
            astNode( AST_TYPE_PLUS,
                astNode( AST_TYPE_TIMES, derive( expr.left, withRespectTo ), expr.right ),
                astNode( AST_TYPE_TIMES, expr.left, derive( expr.right, withRespectTo ) )
            ),
        AST_TYPE_UMINUS: lambda:
            astNode( AST_TYPE_MINUS, derive( expr.left, withRespectTo ) ),
        AST_TYPE_DIVIDE: lambda:
            astNode( AST_TYPE_DIVIDE,
                astNode( AST_TYPE_MINUS,
                    astNode( AST_TYPE_TIMES, derive( expr.left, withRespectTo ), expr.right ),
                    astNode( AST_TYPE_TIMES, expr.left, derive( expr.right, withRespectTo ) )
                ),
                astNode( AST_TYPE_POWER,
                    expr.right,
                    astNode( AST_TYPE_CONST, 2 )
                )
            ),
        AST_TYPE_FUNC: lambda:
            deriveFunc( expr.left, expr.right, withRespectTo )
    }[ expr.astType ]()
