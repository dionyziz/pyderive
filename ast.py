from math import *

AST_TYPE_VAR         =  1                  
AST_TYPE_CONST       =  2                  
AST_TYPE_PLUS        =  3                  
AST_TYPE_MINUS       =  4                  
AST_TYPE_TIMES       =  5                  
AST_TYPE_DIVIDE      =  6                  
AST_TYPE_UMINUS      =  7
AST_TYPE_FUNC        =  8                  
AST_TYPE_POWER       =  9

class astNode( object ):
    astType = 0
    left = None
    right = None
    def __init__( self, astType, left = None, right = None ):
        self.astType = astType
        self.left = left
        self.right = right
    def __repr__( self ):
        return {
            AST_TYPE_VAR: lambda: '[variable ' + self.left + ']',
            AST_TYPE_CONST: lambda: str( self.left ),
            AST_TYPE_PLUS: lambda: '( ' + str( self.left ) + ' + ' + str( self.right ) + ' )',
            AST_TYPE_MINUS: lambda: '( ' + str( self.left ) + ' - ' + str( self.right ) + ' )',
            AST_TYPE_TIMES: lambda: '( ' + str( self.left ) + ' * ' + str( self.right ) + ' )',
            AST_TYPE_UMINUS: lambda: '( -' + str( self.left ) + ' )',
            AST_TYPE_DIVIDE: lambda: '( ' + str( self.left ) + ' / ' + str( self.right ) + ' )',
            AST_TYPE_FUNC: lambda: str( self.left ) + ' ( ' + str( self.right ) + ' )',
            AST_TYPE_POWER: lambda: str( self.left ) + '^' + str( self.right )
        }[ self.astType ]()
