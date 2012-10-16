
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\x05\xec=\xc4\x0380\xda\x00}\xd8\xf0\xc5\x93\xca"'
    
_lr_action_items = {'RPAREN':([2,5,9,15,16,17,18,19,20,21,22,23,],[-10,-9,17,-7,23,-8,-5,-6,-4,-2,-3,-11,]),'FUNC':([0,4,7,8,10,11,12,13,14,],[1,1,1,1,1,1,1,1,1,]),'POWER':([2,5,6,9,15,16,17,18,19,20,21,22,23,],[-10,-9,11,11,-7,11,-8,-5,11,-4,-2,-3,-11,]),'TIMES':([2,5,6,9,15,16,17,18,19,20,21,22,23,],[-10,-9,12,12,-7,12,-8,-5,12,-4,12,12,-11,]),'PLUS':([2,5,6,9,15,16,17,18,19,20,21,22,23,],[-10,-9,13,13,-7,13,-8,-5,13,-4,-2,-3,-11,]),'LPAREN':([0,1,4,7,8,10,11,12,13,14,],[4,8,4,4,4,4,4,4,4,4,]),'VAR':([0,4,7,8,10,11,12,13,14,],[2,2,2,2,2,2,2,2,2,]),'CONST':([0,4,7,8,10,11,12,13,14,],[5,5,5,5,5,5,5,5,5,]),'$end':([2,3,5,6,15,17,18,19,20,21,22,23,],[-10,0,-9,-1,-7,-8,-5,-6,-4,-2,-3,-11,]),'MINUS':([0,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,],[7,-10,7,-9,14,7,7,14,7,7,7,7,7,-7,14,-8,-5,14,-4,-2,-3,-11,]),'DIVIDE':([2,5,6,9,15,16,17,18,19,20,21,22,23,],[-10,-9,10,10,-7,10,-8,-5,10,-4,10,10,-11,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,4,7,8,10,11,12,13,14,],[6,9,15,16,18,19,20,21,22,]),'statement':([0,],[3,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> statement","S'",1,None,None,None),
  ('statement -> expression','statement',1,'p_statement_expr','/home/dionyziz/pyderive/parser.py',55),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','/home/dionyziz/pyderive/parser.py',59),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','/home/dionyziz/pyderive/parser.py',60),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','/home/dionyziz/pyderive/parser.py',61),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','/home/dionyziz/pyderive/parser.py',62),
  ('expression -> expression POWER expression','expression',3,'p_expression_binop','/home/dionyziz/pyderive/parser.py',63),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','/home/dionyziz/pyderive/parser.py',72),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','/home/dionyziz/pyderive/parser.py',76),
  ('expression -> CONST','expression',1,'p_expression_const','/home/dionyziz/pyderive/parser.py',80),
  ('expression -> VAR','expression',1,'p_expression_var','/home/dionyziz/pyderive/parser.py',84),
  ('expression -> FUNC LPAREN expression RPAREN','expression',4,'p_exression_func','/home/dionyziz/pyderive/parser.py',88),
]
