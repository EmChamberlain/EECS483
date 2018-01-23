import sys
import lex as lex

# Used ply documentation example as a starting point http://www.dabeaz.com/ply/example.html

tokens = ('at', 'case', 'class', 'colon', 'comma', 'divide',
          'dot', 'else', 'equals', 'esac', 'false', 'fi',
          'identifier', 'if', 'in', 'inherits', 'integer',
          'isvoid', 'larrow', 'lbrace', 'le', 'let', 'loop',
          'lparen', 'lt', 'minus', 'new', 'not', 'of', 'plus',
          'pool', 'rarrow', 'rbrace', 'rparen', 'semi', 'string',
          'then', 'tilde', 'times', 'true', 'type', 'while', 'line_comment', 'multiline_comment')

# Tokens
t_at = r'@'
t_colon = r':'
t_comma = r','
t_divide = r'/'
t_dot = r'\.'
t_equals = r'='
t_larrow = r'<-'
t_lbrace = r'{'
t_le = r'<='
t_lparen = r'\('
t_lt = r'<'
t_minus = r'-'
t_plus = r'\+'
t_rarrow = r'=>'
t_rbrace = r'}'
t_rparen = r'\)'
t_semi = r';'
t_tilde = r'~'
t_times = r'\*'
t_line_comment = r'--.*'

# Ignored characters
t_ignore = " \f\r\t\v"

# this is the list of reserved keywords
reserved = ['case', 'class', 'else', 'esac', 'false',
            'fi', 'if', 'in', 'inherits', 'isvoid', 'let', 'loop',
            'new', 'not', 'of', 'pool', 'then', 'true', 'while']

# checks lowercase words
def t_lowerword(t):
    r'[a-z][a-zA-Z0-9_]*'
    if t.value.lower() in reserved:  # checking for keywords
        t.type = t.value.lower()
    else:
        t.type = "identifier"
    return t
# checks uppercase words
def t_upperword(t):
    r'[A-Z][a-zA-Z0-9_]*'
    if t.value.lower() == 'false' or t.value.lower() == 'true':  # true and false have special keyword handling
        if t.value[0] == 'f':
            t.type = 'false'
            return t
        elif t.value[0] == 't':
            t.type = 'true'
            return t
        else:
            t.type = 'type'
            return t

    if t.value.lower() in reserved:  # checking for keywords
        t.type = t.value.lower()
    else:
        t.type = "type"
    return t

# incrementing the line count
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# the following conditional lexing for multi-line comments was started using http://www.dabeaz.com/ply/ply.html#ply_nn21
# declaring the states I need for multi-line comments and strings
states = (
    ('multilinecomment', 'exclusive'),
    ('string', 'exclusive'))

# match the first (*, mark the starting location, initialize the level, and then enter the multilinecomment state.
def t_multilinecomment(t):
    r'\(\*'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('multilinecomment')

# add a nested level when we see a new comment
def t_multilinecomment_open(t):
    r'\(\*'
    t.lexer.level += 1

# lower the nested level when we see the end of a comment
def t_multilinecomment_close(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:  # we are now done with the comment
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos]
        t.type = "multiline_comment"
        # t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        return t
# counting newlines as they come
def t_multilinecomment_newline(t):
    r'\n'
    t.lexer.lineno += 1
# do nothing on everything else
def t_multilinecomment_everything(t):
    r'.'
    pass

t_multilinecomment_ignore = " \t"

def t_multilinecomment_error(t):
    # t.lexer.skip(1)
    t_error(t)

# error out on EOF
def t_multilinecomment_eof(t):
    t_error(t)


# match the first quote, mark the starting location, and then enter the state string
def t_string(t):
    r'\"'
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.begin('string')

# error out on NUL
def t_string_nul(t):
    r'\0'
    t_error(t)

# error out on newlines
def t_string_newline(t):
    r'\n'
    t_error(t)

# allow escaped quotes and other things to not end the string
def t_string_escaped(t):
    r'\\.'
    if t.value[1] == '\0':  # error out on \0
        t_error(t)
    pass

# first non-escaped quote ends the string
def t_string_end(t):
    r'"'
    # if t.lexer.lexdata[t.lexer.lexpos - 2] == '\\':  # this is ignoring backslashed quotes just incase
        # return
    t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos - 1]
    if len(t.value) > 1024:  # cool does not allow string too large
        t_error(t)
    t.type = "string"
    t.lexer.begin('INITIAL')
    return t

# do nothing on everything else
def t_string_everything(t):
    r'.'
    pass

t_string_ignore = " "

def t_string_error(t):
    t_error(t)

# error out on EOF
def t_string_eof(t):
    t_error(t)

def t_integer(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
        if t.value < 0 or t.value > 2147483647:  # cool does not allow larger than signed POSITIVE 32-bit ints
            t_error(t)
    except ValueError:
        t_error(t)
    return t


def t_error(t):

    print "ERROR: " + str(lexer.lineno) + ": Lexer: Illegal Character ",
    try:
        print(str(t.value[0]))
    except:
        print(str(t.value))
    exit(1)

# make lexer
lexer = lex.lex()

# read in data
filename = sys.argv[1]
with open(filename, "r") as f:
    file_string = f.read()
lexer.input(file_string)

# list of types that need to output the optional lexeme
types = ['identifier', 'integer', 'string', 'type']

# list of ignored types
ignored_types = ['line_comment', 'multiline_comment']

# create tokens
out_string = ""
while True:
    tok = lexer.token()
    if not tok:
        break
    if tok.type in ignored_types:
        # print(tok.type + ":" + str(tok.lineno))
        continue
    out_string += str(tok.lineno) + "\n"
    out_string += str(tok.type) + "\n"
    if tok.type in types:
        out_string += str(tok.value) + "\n"


with open(filename + "-lex", "w+") as f:
    f.write(out_string)







