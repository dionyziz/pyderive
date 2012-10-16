from ast import *

tokens = (
    'VAR', 'CONST',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN',
    'FUNC'
)

# Tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_POWER   = r'\^'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_FUNC    = r'sin|cos|tan|exp|ln'
t_VAR     = r'[a-z]'

def t_CONST( t ):
    r'\d+(\.\d+)?'
    t.value = float( t.value )
    return t

# Ignored characters
t_ignore = " \t"

def t_newline( t ):
    r'\n+'
    t.lexer.lineno += t.value.count( "\n" )
    
def t_error(t):
    print( "Illegal character '%s'" % t.value[ 0 ] )
    t.lexer.skip( 1 )
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
    ( 'right', 'POWER' ),
    ( 'right', 'UMINUS' )
)

# dictionary of names
names = {}

def p_statement_expr( t ):
    'statement : expression'
    t[ 0 ] = t[ 1 ]

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression POWER expression'''
    t[ 0 ] = {
        '+': lambda: astPlus( t[ 1 ], t[ 3 ] ),
        '-': lambda: astMinus( t[ 1 ], t[ 3 ] ),
        '*': lambda: astTimes( t[ 1 ], t[ 3 ] ),
        '/': lambda: astDivide( t[ 1 ], t[ 3 ] ),
        '^': lambda: astPower( t[ 1 ], t[ 3 ] )
    }[ t[ 2 ] ]()

def p_expression_uminus( t ):
    'expression : MINUS expression %prec UMINUS'
    t[ 0 ] = astUminus( t[ 2 ] )

def p_expression_group( t ):
    'expression : LPAREN expression RPAREN'
    t[ 0 ] = t[ 2 ]

def p_expression_const( t ):
    'expression : CONST'
    t[ 0 ] = astConst( t[ 1 ] )

def p_expression_var( t ):
    'expression : VAR'
    t[ 0 ] = astVar( t[ 1 ] )

def p_exression_func( t ):
    'expression : FUNC LPAREN expression RPAREN'
    t[ 0 ] = astFunc( t[ 1 ], t[ 3 ] )

def p_error( t ):
    print( "Syntax error at '%s'" % t.value )

import ply.yacc as yacc
yacc.yacc()

def parse( s ):
    return yacc.parse( s )
