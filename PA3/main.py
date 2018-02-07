import sys

from lex import LexToken
import yacc as yacc

# reading in the lines in a pythonic way
lines = None
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
EOF_lineno = 0 #  this is for an EOF error later where we might need the lineno

# get the tokens like in the video guide
def read_token():
    global lines
    to_return = lines[0].rstrip('\r\n')  # not fully tested but this seems to preserve string literal whitespace
    lines = lines[1:]
    return to_return


# read in tokens using read_token() like in the video guide
in_tokens = []
while lines:
    lineno = read_token()
    type = read_token()

    if type in ['identifier', 'integer', 'string', 'type']:
        lexeme = read_token()
    else:
        lexeme = type
    in_tokens += [(lineno, type.upper(), lexeme)]


# Custom lexer object like in the video guide
class Lexer(object):
    def token(whatever):
        global in_tokens
        global EOF_lineno
        if not in_tokens:
            return None
        (lineno, type, lexeme) = in_tokens[0]
        in_tokens = in_tokens[1:]
        tok = LexToken()
        tok.type = type
        tok.value = lexeme
        tok.lineno = lineno
        tok.lexpos = 0

        EOF_lineno = lineno  # this keeps track of the most recent lineno
        return tok

# list of terminators
tokens = (
    'AT',
    'CASE',
    'CLASS',
    'COLON',
    'COMMA',
    'DIVIDE',
    'DOT',
    'ELSE',
    'EQUALS',
    'ESAC',
    'FALSE',
    'FI',
    'IDENTIFIER',
    'IF',
    'IN',
    'INHERITS',
    'INTEGER',
    'ISVOID',
    'LARROW',
    'LBRACE',
    'LE',
    'LET',
    'LOOP',
    'LPAREN',
    'LT',
    'MINUS',
    'NEW',
    'NOT',
    'OF',
    'PLUS',
    'POOL',
    'RARROW',
    'RBRACE',
    'RPAREN',
    'SEMI',
    'STRING',
    'THEN',
    'TILDE',
    'TIMES',
    'TRUE',
    'TYPE',
    'WHILE',
)

# precedence
precedence = (
    ('left', 'IN'),  # im not positive IN needs to be less binding than LARROW
    ('right', 'LARROW'),
    ('left', 'NOT'),
    ('nonassoc', 'LE', 'LT', 'EQUALS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'ISVOID'),
    ('left', 'TILDE'),
    ('left', 'AT'),
    ('left', 'DOT'),

)


# rules
# error rule
def p_error(p):
    if p:
        print("ERROR: " + str(p.lineno)
              + ": Parser: syntax error near " + str(p.value)
              + " | parse type: " + str(p.type))
    else:
        print("EORROR: " + str(EOF_lineno)
              + ": Parser: syntax error near EOF")

# classlist rules
def p_program_firstclasslist(p):
    'program : firstclasslist'
    p[0] = p[1]

def p_firstclasslist(p):
    'firstclasslist : class SEMI classlist'
    p[0] = [p[1]] + p[3]

def p_classlist_epsilon(p):
    'classlist : '
    p[0] = []

def p_classlist_class(p):
    'classlist : class SEMI classlist'
    p[0] = [p[1]] + p[3]

# class rules
def p_class_noinherits(p):
    'class : CLASS type LBRACE featurelist RBRACE'
    p[0] = (p.lineno(1), 'no_inherits', p[2], p[4])

def p_class_inherits(p):
    'class : CLASS type INHERITS type LBRACE featurelist RBRACE'
    p[0] = (p.lineno(1), 'inherits', p[2], p[4], p[6])

# type rule
def p_type(p):
    'type : TYPE'
    p[0] = (p.lineno(1), 'type', p[1])

# featurelist rules
def p_featurelist_epsilon(p):
    'featurelist : '
    p[0] = []

def p_featurelist_feature(p):
    'featurelist : feature SEMI featurelist'
    p[0] = [p[1]] + p[3]

# feature rules
def p_feature_method(p):
    'feature : identifier LPAREN formallistfirst RPAREN COLON type LBRACE exp RBRACE'
    p[0] = (p[1][0], 'method', p[1], p[3], p[6], p[8])

def p_feature_attributenoinit(p):
    'feature : identifier COLON type'
    p[0] = (p[1][0], 'attribute_no_init', p[1], p[3])

def p_feature_attributeinit(p):
    'feature : identifier COLON type LARROW exp'
    p[0] = (p[1][0], 'attribute_init', p[1], p[3], p[5])


# formallist rules
def p_formallist_restsolo(p):
    'formallistrest : formal'
    p[0] = [p[1]]

def p_formallist_rest(p):
    'formallistrest : formal COMMA formallistrest'
    p[0] = [p[1]] + p[3]

def p_formallist_firstepsilon(p):
    'formallistfirst : '
    p[0] = []

def p_formallist_firstsolo(p):
    'formallistfirst : formal'
    p[0] = [p[1]]

def p_formallist_first(p):
    'formallistfirst : formal COMMA formallistrest'
    p[0] = [p[1]] + p[3]

# formal rule
def p_formal(p):
    'formal : identifier COLON type'
    p[0] = (p[1][0], 'formal', p[1], p[3])

# identifier rule
def p_identifier(p):
    'identifier : IDENTIFIER'
    p[0] = (p.lineno(1), 'identifier', p[1])


# explist comma delimited rules
def p_explistcomma_single(p):  # this single is to take care of the end of the list
    'explistcommarest : exp'
    p[0] = [p[1]]

def p_explistcomma_rest(p):
    'explistcommarest : exp COMMA explistcommarest'
    p[0] = [p[1]] + p[3]


def p_explistcomma_firstepsilon(p):  # this is to take care of no exps
    'explistcommafirst : '
    p[0] = []

def p_explistcomma_firstsolo(p):  # this is to take care of one exp
    'explistcommafirst : exp'
    p[0] = [p[1]]

def p_explistcomma_first(p):
    'explistcommafirst : exp COMMA explistcommarest'
    p[0] = [p[1]] + p[3]

# explist semicolon delimited rules
def p_explistsemi_epsilon(p):
    'explistsemirest : '
    p[0] = []

def p_explistsemi_rest(p):
    'explistsemirest : exp SEMI explistsemirest'
    p[0] = [p[1]] + p[3]

def p_explistsemi_first(p):
    'explistsemifirst : exp SEMI explistsemirest'
    p[0] = [p[1]] + p[3]



# exp rules
# basic exp rules
def p_exp_assign(p):
    'exp : identifier LARROW exp'
    p[0] = (p[1][0], 'assign', p[1], p[3])

def p_exp_identifier(p):
    'exp : identifier'
    p[0] = (p[1][0], 'identifier', p[1])

def p_exp_integer(p):
    'exp : INTEGER'
    p[0] = (p.lineno(1), 'integer', int(p[1]))

def p_exp_string(p):
    'exp : STRING'
    p[0] = (p.lineno(1), 'string', p[1])

def p_exp_true(p):
    'exp : TRUE'
    p[0] = (p.lineno(1), 'true', p[1])

def p_exp_false(p):
    'exp : FALSE'
    p[0] = (p.lineno(1), 'false', p[1])

def p_exp_plus(p):
    'exp : exp PLUS exp'
    p[0] = (p[1][0], 'plus', p[1], p[3])

def p_exp_minus(p):
    'exp : exp MINUS exp'
    p[0] = (p[1][0], 'minus', p[1], p[3])

def p_exp_times(p):
    'exp : exp TIMES exp'
    p[0] = (p[1][0], 'times', p[1], p[3])

def p_exp_divide(p):
    'exp : exp DIVIDE exp'
    p[0] = (p[1][0], 'divide', p[1], p[3])

# dispatch exp rules
def p_exp_dynamicdispatch(p):
    'exp : exp DOT identifier LPAREN explistcommafirst RPAREN'
    p[0] = (p[1][0], 'dynamic_dispatch', p[1], p[3], p[5])

def p_exp_staticdispatch(p):
    'exp : exp AT type DOT identifier LPAREN explistcommafirst RPAREN'
    p[0] = (p[1][0], 'static_dispatch', p[1], p[3], p[5], p[7])

def p_exp_selfdispatch(p):
    'exp : identifier LPAREN explistcommafirst RPAREN'
    p[0] = (p[1][0], 'self_dispatch', p[1], p[3])

# block exp rules
def p_exp_if(p):
    'exp : IF exp THEN exp ELSE exp FI'
    p[0] = (p.lineno(1), 'if', p[2], p[4], p[6])

def p_exp_while(p):
    'exp : WHILE exp LOOP exp POOL'
    p[0] = (p.lineno(1), 'while', p[2], p[4])

def p_exp_block(p):
    'exp : LBRACE explistsemifirst RBRACE'
    p[0] = (p.lineno(1), 'block', p[2])

# binding rules
def p_binding_noinit(p):
    'binding : identifier COLON type'
    p[0] = (p[1][0], 'let_binding_no_init', p[1], p[3])

def p_binding_init(p):
    'binding : identifier COLON type LARROW exp'
    p[0] = (p[1][0], 'let_binding_init', p[1], p[3], p[5])

# binding list rules
def p_bindinglist_epsilon(p):
    'bindinglistrest : '
    p[0] = []

def p_bindinglist_single(p): # this single is to take care of the end of the list
    'bindinglistrest : binding'
    p[0] = [p[1]]

def p_bindinglist_rest(p):
    'bindinglistrest : binding COMMA bindinglistrest'
    p[0] = [p[1]] + p[3]

def p_bindinglist_firstonly(p): # this is to take care of just one binding
    'bindinglistfirst : binding'
    p[0] = [p[1]]

def p_bindinglist_first(p):
    'bindinglistfirst : binding COMMA bindinglistrest'
    p[0] = [p[1]] + p[3]

# let rule
def p_exp_let(p):
    'exp : LET bindinglistfirst IN exp'
    p[0] = (p.lineno(1), 'let', p[2], p[4])

# case elem list rules
def p_caseelemlist_epsilon(p):
    'caseelemlistrest : '
    p[0] = []

def p_caseelemlist_rest(p):
    'caseelemlistrest : caseelem SEMI caseelemlistrest'
    p[0] = [p[1]] + p[3]

def p_caseelemlist_first(p):
    'caseelemlistfirst : caseelem SEMI caseelemlistrest'
    p[0] = [p[1]] + p[3]

# case elem rules
def p_caseelem(p):
    'caseelem : identifier COLON type RARROW exp'
    p[0] = (p[1], p[3], p[5])

# case rule
def p_exp_case(p):
    'exp : CASE exp OF caseelemlistfirst ESAC'
    p[0] = (p.lineno(1), 'case', p[2], p[4])

# simple rules
def p_exp_new(p):
    'exp : NEW type'
    p[0] = (p.lineno(1), 'new', p[2])

def p_exp_isvoid(p):
    'exp : ISVOID exp'
    p[0] = (p.lineno(1), 'isvoid', p[2])

# comparison rules
def p_exp_lt(p):
    'exp : exp LT exp'
    p[0] = (p[1][0], 'lt', p[1], p[3])

def p_exp_le(p):
    'exp : exp LE exp'
    p[0] = (p[1][0], 'le', p[1], p[3])

def p_exp_eq(p):
    'exp : exp EQUALS exp'
    p[0] = (p[1][0], 'eq', p[1], p[3])

def p_exp_not(p):
    'exp : NOT exp'
    p[0] = (p.lineno(1), 'not', p[2])
def p_exp_negate(p):
    'exp : TILDE exp'
    p[0] = (p.lineno(1), 'negate', p[2])

# paren rule
def p_exp_parens(p):
    'exp : LPAREN exp RPAREN'
    p[0] = (p.lineno(1), 'paren', p[2])

# Actually parse the input
custom_lexer = Lexer()
parser = yacc.yacc()
ast = parser.parse(lexer=custom_lexer)


# Properly output the ast
out_filename = (sys.argv[1])[:-3] + "ast"
out_string = ""

# list output
def list_str(ast, list_method):  # list_str is a method just like the video guide, list_method is a string method
    global out_string
    out_string += str(len(ast)) + "\n"
    for e in ast:
        list_method(e)


# class output
def class_str(ast):
    global out_string
    identifier_str(ast[2])
    out_string += str(ast[1]) + "\n"
    if ast[1] == 'inherits':
        identifier_str(ast[3])
        list_str(ast[4], feature_str)
    elif ast[1] == 'no_inherits':
        list_str(ast[3], feature_str)
    else:
        print('class_str defaulted')
        exit(1)


# identifier/type output, using this function for identifiers and types
def identifier_str(ast):
    global out_string
    out_string += str(ast[0]) + "\n" + ast[2] + "\n"

# feature output
def feature_str(ast):
    global out_string
    out_string += ast[1] + "\n"
    if ast[1] == "attribute_no_init":
        identifier_str(ast[2])
        identifier_str(ast[3])
    elif ast[1] == "attribute_init":
        identifier_str(ast[2])
        identifier_str(ast[3])
        exp_str(ast[4])
    elif ast[1] == "method":
        identifier_str(ast[2])
        list_str(ast[3], formal_str)
        identifier_str(ast[4])
        exp_str(ast[5])
    else:
        print("feature_str defaulted")
        exit(1)


# expression output
def exp_str(ast):  # could possibly break this function down more but I dont think it would be more readable
    global out_string
    if ast[1] == 'paren':  # this skips the auto output for the paren expression
        exp_str(ast[2])
        return
    out_string += str(ast[0]) + "\n" + ast[1] + "\n"
    if ast[1] == 'assign':
        identifier_str(ast[2])
        exp_str(ast[3])
    elif ast[1] == 'identifier':
        identifier_str(ast[2])
    elif ast[1] in ['plus', 'minus', 'times', 'divide']:
        exp_str(ast[2])
        exp_str(ast[3])
    elif ast[1] == 'dynamic_dispatch':
        exp_str(ast[2])
        identifier_str(ast[3])
        list_str(ast[4], exp_str)
    elif ast[1] == 'static_dispatch':
        exp_str(ast[2])
        identifier_str(ast[3])
        identifier_str(ast[4])
        list_str(ast[5], exp_str)
    elif ast[1] == 'self_dispatch':
        identifier_str(ast[2])
        list_str(ast[3], exp_str)
    elif ast[1] == 'if':
        exp_str(ast[2])
        exp_str(ast[3])
        exp_str(ast[4])
    elif ast[1] == 'while':
        exp_str(ast[2])
        exp_str(ast[3])
    elif ast[1] == 'block':
        list_str(ast[2], exp_str)
    elif ast[1] == 'let':
        list_str(ast[2], binding_str)
        exp_str(ast[3])
    elif ast[1] == 'case':
        exp_str(ast[2])
        list_str(ast[3], caseelem_str)
    elif ast[1] == 'new':
        identifier_str(ast[2])
    elif ast[1] == 'isvoid':
        exp_str(ast[2])
    elif ast[1] in  ['lt', 'le', 'eq']:
        exp_str(ast[2])
        exp_str(ast[3])
    elif ast[1] in ['not', 'negate']:
        exp_str(ast[2])
    elif ast[1] in ['integer', 'string']:
        out_string += str(ast[2]) + "\n"
    elif ast[1] in ['true', 'false']:
        pass
    else:
        print('exp_str defaulted')
        exit(1)

# formal output
def formal_str(ast):
    identifier_str(ast[2])
    identifier_str(ast[3])

# binding output
def binding_str(ast):
    global out_string
    out_string += ast[1] + "\n"
    if ast[1] == 'let_binding_no_init':
        identifier_str(ast[2])
        identifier_str(ast[3])
    elif ast[1] == 'let_binding_init':
        identifier_str(ast[2])
        identifier_str(ast[3])
        exp_str(ast[4])
    else:
        print('binding_str defaulted')
        exit(1)

# case element output
def caseelem_str(ast):
    global out_string
    identifier_str(ast[0])
    identifier_str(ast[1])
    exp_str(ast[2])

# output the program recusively which is a list of classes
list_str(ast, class_str)
# write the program to file
with open(out_filename, 'w+') as f:
    f.write(out_string)





