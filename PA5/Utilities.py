class FP(object):
    def __init__(self, offset=None):
        self.offset = offset

    def __str__(self):
        if self.offset == None:
            return "fp"
        else:
            return "fp[%d]" % self.offset


class SP(object):
    def __init__(self, offset=None):
        self.offset = offset

    def __str__(self):
        if self.offset == None:
            return "sp"
        else:
            return "sp[%d]" % self.offset

class R(object):
    def __init__(self, id, offset=None):
        self.id = id
        self.offset = offset

    def off(self, offset):
        return R(self.id, offset)

    def __str__(self):
        if self.offset == None:
            return "r%d" % self.id
        else:
            return "r%d[%d]" % (self.id, self.offset)

output = ""

rself = R(0)
racc = R(1)
rtmp = R(2)

vtable_object_offset = 0
vtable_new_offset = 1
vtable_methods_offset = 2

vtable_offset = 0
size_offset = 1
attributes_offset = 2


def pr(in_str):
    global output
    output += "\t\t" + in_str + "\n"

def log(in_str):
    global output
    output += "\t\t;; " + in_str + "\n"

def call(call_reg):
    pr("push fp")
    pr("push %s" % rself)
    # pr("debug %s" % call_reg)
    pr("call %s" % call_reg)
    pr("pop %s" % rself)
    pr("pop fp")

def callee_init():
    pr("mov fp <- sp")
    pr("push ra")

def ret(return_register):
    pr("mov %s <- %s" % (racc, return_register))
    pr("pop ra")
    pr("return")

def new_section(title, indention):
    global output
    output += ("\t\t" * indention) + ";; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n"
    output += ("\t\t" * indention) + ";; %s\n" % title





"""
def cgen(exp):

    # assign
    if isinstance(exp, AST.Assign):
        var = get_identifier()
        rhs = get_type_expression()
        return AST.Assign(lineno, var, rhs)
    #
    elif isinstance(exp, AST.Dynamic_Dispatch):
        e = get_type_expression()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        return AST.Dynamic_Dispatch(lineno, e, method, args)
    #
    elif isinstance(exp, AST.Static_Dispatch):
        e = get_type_expression()
        type = get_identifier()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        return AST.Static_Dispatch(lineno, e, type, method, args)

    elif isinstance(exp, AST.Self_Dispatch):
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        return AST.Self_Dispatch(lineno, method, args)

    elif isinstance(exp, AST.If):
        pred = get_type_expression()
        then = get_type_expression()
        else_exp = get_type_expression()
        return AST.If(lineno, pred, then, else_exp)

    elif isinstance(exp, AST.While):
        pred = get_type_expression()
        body = get_type_expression()
        return AST.While(lineno, pred, body)

    elif isinstance(exp, AST.Block):
        body_exp_list = []
        num_body_exp = int(get_line())
        for i in range(num_body_exp):
            body_exp_list.append(get_type_expression())
        return AST.Block(lineno, body_exp_list)

    elif isinstance(exp, AST.New):
        class_id = get_identifier()
        return AST.New(lineno, class_id)
    elif isinstance(exp, AST.Isvoid):
        e = get_type_expression()
        return AST.Isvoid(lineno, e)

    elif isinstance(exp, AST.Plus):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Plus(lineno, x, y)

    elif isinstance(exp, AST.Minus):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Minus(lineno, x, y)

    elif isinstance(exp, AST.Times):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Times(lineno, x, y)

    elif isinstance(exp, AST.Divide):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Divide(lineno, x, y)

    elif isinstance(exp, AST.Lt):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Lt(lineno, x, y)

    elif isinstance(exp, AST.Le):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Le(lineno, x, y)

    elif isinstance(exp, AST.Eq):
        x = get_type_expression()
        y = get_type_expression()
        return AST.Eq(lineno, x, y)

    elif isinstance(exp, AST.Not):
        x = get_type_expression()
        return AST.Not(lineno, x)

    elif isinstance(exp, AST.Negate):
        x = get_type_expression()
        return AST.Negate(lineno, x)

    elif isinstance(exp, AST.Integer):
        int_const = int(get_line())
        return AST.Integer(lineno, int_const)

    elif isinstance(exp, AST.String):
        str_const = get_line()
        return AST.String(lineno, str_const)

    elif isinstance(exp, AST.Identifier_Exp):
        var = get_identifier()
        return AST.Identifier_Exp(lineno, var)

    elif isinstance(exp, AST.True_Exp):
        return AST.True_Exp(lineno)

    elif isinstance(exp, AST.False_Exp):
        return AST.False_Exp(lineno)

    elif isinstance(exp, AST.Let):
        bindings = []
        num_bindings = int(get_line())
        for i in range(num_bindings):
            bindings.append(get_binding())
        body = get_type_expression()
        return AST.Let(lineno, bindings, body)

    elif isinstance(exp, AST.Case):
        case_exp = get_type_expression()
        case_elems = []
        num_elems = int(get_line())
        for i in range(num_elems):
            case_elems.append(get_case_elem())
        return AST.Case(lineno, case_exp, case_elems)

    elif isinstance(exp, AST.Internal):
        return AST.Internal(lineno, get_line())

    else:
        print("Cgen switch defaulted: " + str(name))
        exit(1)
"""