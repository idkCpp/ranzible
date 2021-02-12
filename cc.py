
tokens = [
        'NL',
        'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY',
        'NUMBER', 'STRING', 'IDENTIFIER', 'ZERO',
        'SAME', 'DIFFERENT', 'COLON', 'SEMICOLON', 'MEMBER', 'COMMA', 'BITOR', 'OR', 'BITAND', 'AND'
        ]

reserved = {
        'play': 'PLAY',
        'role': 'ROLE',
        'block': 'BLOCK',
        'variable': 'VARIABLE',
        'null': 'NULL',
        'depends': 'DEPENDS',
        'on': 'ON',
        'host': 'HOST',
        'block': 'BLOCK',
        'module': 'MODULE',
        'if': 'IF',
        'when': 'WHEN',
        'and': 'TEXT_AND',
        'or': 'TEXT_OR',
        'not': 'TEXT_NOT',
        'register': 'REGISTER',
        }

tokens += reserved.values()

t_ignore = " \t"
t_MEMBER = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_STRING = r'"([^"]|\\")*"|\'([^\']|\\\')*\''
#t_STAR = r'\*'
#t_EXCLAMATION_MARK = r'!'
t_BITAND = r'&(?!&)'
t_AND = r'&&'
t_BITOR = r'\|(?!\|)'
t_OR = r'\|\|'
#t_EQ = r'=(?!=)'
t_SAME = r'=='
t_DIFFERENT = r'!='
t_COLON = r':'
t_SEMICOLON = r';'
t_ZERO = r'(?<![0-9.])0(?![0-9.])'

def t_IDENTIFIER(t):
    r'[a-zA-Z]\w*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

def t_NL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def p_document(p):
    '''document : document top_level_definition
                | top_level_definition
                |'''
    if len(p) == 1:
        p[0] = ('DOC', [])
    elif len(p) == 2:
        p[0] = ('DOC', [ p[1] ])
    else:
        p[0] = p[1]
        p[0][1].append(p[2])

def p_top_level_definition(p):
    '''top_level_definition : role_definition'''
                            #| play_definition

def p_role_definition(p):
    'role_definition : ROLE IDENTIFIER LPAREN possibly_tagged_param_seq RPAREN depends_clause_seq LCURLY role_body RCURLY'
    p[0] = ('ROLE', p[2], p[4], p[6], p[8])

def p_possibly_tagged_param_seq(p):
    '''possibly_tagged_param_seq : possibly_tagged_param_seq COMMA possibly_tagged_param
                                 | possibly_tagged_param
                                 |'''
    if len(p) == 2:
        p[0] = ('PARAM_SEQ', [ p[1] ])
    elif len(p) == 4:
        p[0] = p[1]
        p[0][1].append(p[3])
    elif len(p) == 1:
        p[0] = ('PARAM_SEQ', [])

def p_possibly_tagged_param(p):
    '''possibly_tagged_param : param
                             | LBRACKET IDENTIFIER RBRACKET param'''
    if len(p) == 2:
        p[0] = p[1] # simple param
    elif len(p) == 5:
        p[0] = ('TAGGED-PARAM', p[4], p[2] ) # tagged param

def p_param_seq(p):
    '''param_seq : param_seq COMMA param
                 | param
                 |'''
    if len(p) == 2:
        p[0] = ('PARAM_SEQ', [ p[1] ])
    elif len(p) == 4:
        p[0] = p[1]
        p[0][1].append(p[3])
    elif len(p) == 1:
        p[0] = ('PARAM_SEQ', [])

def p_param(p):
    '''param : IDENTIFIER
             | IDENTIFIER COLON expression'''
    if len(p) == 2:
        p[0] = ('PARAM', p[1], None) # simple param
    elif len(p) == 5:
        p[0] = ('PARAM', p[2], p[4] ) # param with default

def p_depends_clause_seq(p):
    '''depends_clause_seq : depends_clause_seq COMMA depends_clause
                          | depends_clause
                          |'''
    if len(p) == 1:
        p[0] = ('DEPENDS', [])
    elif len(p) == 2:
        p[0] = ('DEPENDS', [ p[1] ])
    elif len(p) == 4:
        p[0] = p[1]
        p[1][1].append(p[3])

def p_optional_depends_clause(p):
    '''depends_clause : DEPENDS ON IDENTIFIER LPAREN param_seq RPAREN
                      | DEPENDS IDENTIFIER LPAREN param_seq RPAREN'''
    if len(p) == 7:
        p[0] = ('DEPENDENCY', p[3], p[5])
    else:
        p[0] = ('DEPENDENCY', p[2], p[4])

def p_role_body(p):
    '''role_body : role_body role_statement
                 | role_statement
                 |'''
    if len(p) == 3:
        p[0] = p[1]
        p[0][1].append(p[2])
    elif len(p) == 2:
        p[0] = ('ROLE_BODY', [ p[1] ])
    elif len(p) == 1:
        p[0] = ('ROLE_BODY', [] )

def p_role_statement(p):
    '''role_statement : variable_definition SEMICOLON
                      | module_invocation SEMICOLON
                      | control_flow_statement SEMICOLON'''
    p[0] = p[1]

def p_variable_definition(p):
    'variable_definition : VARIABLE scope param_seq'
    p[0] = ('VARIABLE_DEFINITON', p[2], p[3])

def p_module_invocation(p):
    '''module_invocation : unnamed_module_invocation
                         | named_module_invocation'''
    p[0] = p[1]

def p_unnamed_module_invocation(p):
    '''unnamed_module_invocation : MODULE IDENTIFIER LPAREN param_seq RPAREN
                                 | MODULE IDENTIFIER LPAREN param_seq RPAREN REGISTER scope STRING'''
    p[0] = {
            'module_name': p[2],
            'params': p[4]
            }
    if len(p) > 6:
        p[0]['register'] = ( p[7], p[8] )

def p_named_module_invocation(p):
    'named_module_invocation : STRING unnamed_module_invocation'
    p[0] = p[2]
    p[0]['name'] = p[1]

def p_control_flow_statement(p):
    '''control_flow_statement : IF LPAREN expression RPAREN LCURLY role_body RCURLY
                              | WHEN LPAREN expression RPAREN LCURLY role_body RCURLY'''
    p[0] = (p[1], p[3], p[6])

def p_expression(p):
    '''expression : IDENTIFIER
                  | NUMBER
                  | ZERO
                  | NULL
                  | STRING
                  | expression MEMBER expression
                  | expression LBRACKET expression RBRACKET
                  | LPAREN expression RPAREN
                  | expression TEXT_OR expression
                  | expression SAME expression
                  | expression DIFFERENT expression'''
    p[0] = ('EXPR',)

def p_scope(p):
    '''scope : HOST
             | ROLE
             | BLOCK'''

def p_error(p):
    print(f"syntax error on line {p.lineno}: unexpected {p.type} '{p.value}'")

import ply.lex as lex
import ply.yacc as yacc
l = lex.lex()
y = yacc.yacc()
f = open('demo.rz', 'r')
input_data = f.read()
f.close()
if False:
    l.input(input_data)

    while True:
        tok = l.token()
        if not tok:
            break
        print(tok)
else:
    tree = y.parse(input_data, lexer=l)
    print(tree)
