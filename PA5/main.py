import sys

import AST
import Utilities
from Utilities import pr as pr
from Utilities import log as log
from Utilities import call as call
from Utilities import call_new as call_new
from Utilities import callee_init as callee_init
from Utilities import ret as ret
from Utilities import new_section as new_section

in_lines = []

def get_line():
    global in_lines
    return in_lines.pop(0)

def get_identifier():
    lineno = get_line()
    id = get_line()
    return AST.Identifier(lineno, id)




def get_binding():
    name = get_line()
    var = get_identifier()
    type = get_identifier()
    val = None
    if name == "let_binding_init":
        val = get_type_expression()
    return AST.Binding(var, type, val)

def get_case_elem():
    var = get_identifier()
    type = get_identifier()
    body = get_type_expression()
    return AST.Case_Elem(var, type, body)



def get_expression(lineno):
    name = get_line()

    if name == "assign":
        var = get_identifier()
        rhs = get_type_expression()
        return AST.Assign(lineno, var, rhs)
    elif name == "dynamic_dispatch":
        e = get_type_expression()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        to_return = AST.Dynamic_Dispatch(lineno, e, method, args)
        to_return.exp_type = e.exp_type
        return to_return
    elif name == "static_dispatch":
        e = get_type_expression()
        type = get_identifier()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        return AST.Static_Dispatch(lineno, e, type, method, args)
    elif name == "self_dispatch":
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_type_expression())
        return AST.Self_Dispatch(lineno, method, args)
    elif name == "if":
        pred = get_type_expression()
        then = get_type_expression()
        else_exp = get_type_expression()
        return AST.If(lineno, pred, then, else_exp)
    elif name == "while":
        pred = get_type_expression()
        body = get_type_expression()
        return AST.While(lineno, pred, body)
    elif name == "block":
        body_exp_list = []
        num_body_exp = int(get_line())
        for i in range(num_body_exp):
            body_exp_list.append(get_type_expression())
        return AST.Block(lineno, body_exp_list)
    elif name == "new":
        class_id = get_identifier()
        return AST.New(lineno, class_id)
    elif name == "isvoid":
        e = get_type_expression()
        return AST.Isvoid(lineno, e)
    elif name == "plus":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Plus(lineno, x, y)
    elif name == "minus":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Minus(lineno, x, y)
    elif name == "times":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Times(lineno, x, y)
    elif name == "divide":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Divide(lineno, x, y)
    elif name == "lt":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Lt(lineno, x, y)
    elif name == "le":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Le(lineno, x, y)
    elif name == "eq":
        x = get_type_expression()
        y = get_type_expression()
        return AST.Eq(lineno, x, y)
    elif name == "not":
        x = get_type_expression()
        return AST.Not(lineno, x)
    elif name == "negate":
        x = get_type_expression()
        return AST.Negate(lineno, x)
    elif name == "integer":
        int_const = int(get_line())
        return AST.Integer(lineno, int_const)
    elif name == "string":
        str_const = get_line()
        Utilities.strings.append(str_const)
        return AST.String(lineno, str_const, "string%d" % (len(Utilities.strings) - 1))
    elif name == "identifier":
        var = get_identifier()
        return AST.Identifier_Exp(lineno, var)
    elif name == "true":
        return AST.True_Exp(lineno)
    elif name == "false":
        return AST.False_Exp(lineno)
    elif name == "let":
        bindings = []
        num_bindings = int(get_line())
        for i in range(num_bindings):
            bindings.append(get_binding())
        body = get_type_expression()
        return AST.Let(lineno, bindings, body)
    elif name == "case":
        case_exp = get_type_expression()
        case_elems = []
        num_elems = int(get_line())
        for i in range(num_elems):
            case_elems.append(get_case_elem())
        return AST.Case(lineno, case_exp, case_elems)
    elif name == "internal":
        return AST.Internal(lineno, get_line())
    else:
        print("Expression switch defaulted: " + str(name))
        exit(1)

def get_type_expression():
    lineno = get_line()
    type_exp = get_line()
    exp = get_expression(lineno)
    if isinstance(exp, AST.Dynamic_Dispatch):
        return exp
    exp.exp_type = type_exp
    return exp



def get_formal():
    name = get_identifier()
    type = get_identifier()
    return AST.Formal(name, type)


def get_feature():
    feature_str = get_line()
    name = get_identifier()
    type = None
    init = None
    formals_list = []
    body = None


    if feature_str == "attribute_no_init":
        type = get_identifier()
        return AST.Attribute(name, type, init)
    elif feature_str == "attribute_init":
        type = get_identifier()
        init = get_type_expression()
        return AST.Attribute(name, type, init)
    elif feature_str == "method":
        num_formals = int(get_line())

        for i in range(num_formals):
            formals_list.append(get_formal())

        type = get_identifier()
        body = get_type_expression()
        return AST.Method(name, formals_list, type, body)
    else:
        print("Feature switch defaulted: " + str(feature_str))
        exit(1)



def get_class():
    name = get_identifier()
    parent = None
    inherits_str = get_line()
    if inherits_str == "inherits":
        parent = get_identifier()

    features_list = []
    num_features = int(get_line())

    for i in range(num_features):
        features_list.append(get_feature())
    return AST.Class(name, parent, features_list)


def get_attribute():
    init = get_line()
    if init == "no_initializer":
        name = get_line()
        type = get_line()
        return AST.Attribute(name, type, None)
    else:
        name = get_line()
        type = get_line()
        exp = get_type_expression()
        return AST.Attribute(name, type, exp)

def get_method():
    name = get_line()
    num_formals = int(get_line())
    formals = []
    for i in range(num_formals):
        formals.append(AST.Formal(get_line(), None))
    type_id = get_line()
    exp = get_type_expression()
    return AST.Method(name, formals, type_id, exp)


def read_class_map():
    class_map = {}
    get_line()
    num = int(get_line())
    for i in range(num):
        attrs = []
        name = get_line()
        if name == "Bool":
            attrs.append(AST.Attribute("contents", "unboxed_bool", 0))
        if name == "Int":
            attrs.append(AST.Attribute("contents", "unboxed_int", False))
        if name == "String":
            attrs.append(AST.Attribute("contents", "unboxed_string", "the.empty.string"))
        num_attr = int(get_line())
        for j in range(num_attr):
            attrs.append(get_attribute())
        class_map[name] = attrs
    return class_map

def read_implementation_map():
    imp_map = {}
    get_line()
    num_classes = int(get_line())
    for i in range(num_classes):
        class_name = get_line()
        num_methods = int(get_line())
        methods = []
        for j in range(num_methods):
            methods.append(get_method())
        imp_map[class_name] = methods
    return imp_map


def read_parent_map():
    parent_map = {}
    get_line()
    num_relations = int(get_line())
    for i in range(num_relations):
        child = get_line()
        parent = get_line()
        parent_map[child] = parent
    return parent_map




def read_AST():
    ast = []
    num_classes = int(get_line())
    for i in range(num_classes):
        ast.append(get_class())
    return ast



rself = Utilities.rself
racc = Utilities.racc
rtmp = Utilities.rtmp

vtable_object_offset = Utilities.vtable_object_offset
vtable_new_offset = Utilities.vtable_new_offset
vtable_methods_offset = Utilities.vtable_methods_offset

vtable_offset = Utilities.vtable_offset
size_offset = Utilities.size_offset
attributes_offset = Utilities.attributes_offset



def main():
    global in_lines

    with open(sys.argv[1], 'r') as f:
        in_lines = [l.rstrip('\r\n') for l in f.readlines()]

    class_map = read_class_map()
    imp_map = read_implementation_map()
    # parent_map = read_parent_map()
    # TODO: If I start needing ast I need to reimplement string constants
    # ast = read_AST()

    classes = list(class_map.keys())




    # vtables
    new_section("vtables", 0)
    for cls in classes:
        Utilities.output += "%s..vtable:\n" % cls
        Utilities.strings.append(cls)
        pr("constant %s" % "string" + str(len(Utilities.strings) - 1))
        Utilities.string_map[cls] = "string" + str(len(Utilities.strings) - 1)
        pr("constant %s..new" % cls)

        if cls in imp_map:
            for method in imp_map[cls]:
                pr("constant %s.%s" % (method.type_id, method.name_id))

    # globals
    new_section("globals", 0)
    Utilities.output += "the.empty.string:\n\t\t constant \"\"\n"
    Utilities.output += "the.abort.string:\n\t\t constant \"abort\\n\"\n"

    Utilities.output += "the.substring.range.string:\n\t\t constant \"ERROR: 0: Exception: String.substr out of range\\n\"\n"
    for i, string in enumerate(Utilities.strings):
        Utilities.output += "%s:\n\t\t constant \"%s\"\n" % ("string" + str(i), string)


    # constructors
    new_section("constructors", 0)
    for cls in classes:
        Utilities.output += "%s..new:\n" % cls
        callee_init()

        # size
        # object size and vtable
        log("object size and vtable")
        object_size = len(class_map[cls]) + 2
        pr("li %s <- %d" % (rself, object_size))
        pr("alloc %s %s" % (rself, rself))


        # internal attributes
        new_section("internal attributes", 1)
        # vtable
        log("vtable")
        pr("la %s <- %s..vtable" % (rtmp, cls))
        pr("st %s[%d] <- %s" % (rself, vtable_offset, rtmp))
        # object size
        log("object size")
        pr("li %s <- %d" % (rtmp, object_size))
        pr("st %s[%d] <- %s" % (rself, size_offset, rtmp))

        # attributes
        new_section("attributes", 1)
        st = {}
        for i, attr in enumerate(class_map[cls]):

            if attr.type_id == 'unboxed_int':
                pr("li %s <- %d" % (rtmp, attr.init_exp))
                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, rtmp))
                continue
            if attr.type_id == 'unboxed_bool':
                pr("li %s <- %d" % (rtmp, 0 if not attr.init_exp else 1))
                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, rtmp))
                continue
            if attr.type_id == 'unboxed_string':
                pr("la %s <- %s" % (rtmp, attr.init_exp))
                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, rtmp))
                continue

            pr("la %s <- %s..new" % (rtmp, attr.type_id))
            call_new(rtmp)
            if attr.init_exp is not None:

                pr(";; cgen expression initializer %s.%s" % (cls, attr.name_id))

                res = attr.init_exp.cgen(cls, imp_map, st)

                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, res))
            else:
                pr("li %s <- 0" % rtmp)
                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, rtmp))
            st[attr.name_id] = rself.off(attributes_offset + i)
        ret(rself)

    # internal methods
    new_section("internal methods", 0)

    # Utilities.output += "Object.copy:\n"
    # callee_init()
    # pr("ld r2 <- r0[%d]" % size_offset)
    # pr("alloc r1 r2")
    # Utilities.output += "Object.copy.while:\n"
    # pr("bz r2 Object.copy.whileEnd")
    # pr("ld r3 <- r0[0]")
    # pr("st r1[0] <- r3")
    # pr("li r3 <- 1")
    # pr("add r0 <- r0 r3")
    # pr("add r1 <- r1 r3")
    # pr("sub r2 <- r2 r3")
    # pr("jmp Object.copy.while")
    #
    # Utilities.output += "Object.copy.whileEnd:\n"
    # pr("mov r1 <- r0")
    # ret(racc)
    log("abort")
    Utilities.output += "Object.abort:\n"
    callee_init()
    pr("la r1 <- the.abort.string")
    pr("syscall IO.out_string")
    pr("syscall exit")

    log("type_name")
    Utilities.output += "Object.type_name:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "String"))
    new_loc = new.cgen("Object", imp_map, {})

    pr("ld %s <- %s[%d]" % (rtmp, rself, vtable_offset))
    pr("ld %s <- %s[%d]" % (rtmp, rtmp, vtable_object_offset))
    pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))
    ret(racc)

    log("copy")
    Utilities.output += "Object.copy:\n"
    callee_init()
    pr("ld r2 <- r0[%d]" % size_offset)
    pr("alloc r1 r2")
    Utilities.output += "Object.copy.while:\n"
    pr("bz r2 Object.copy.whileEnd")
    pr("ld r3 <- r0[0]")
    pr("st r1[0] <- r3")
    pr("li r3 <- 1")
    pr("add r0 <- r0 r3")
    pr("add r1 <- r1 r3")
    pr("sub r2 <- r2 r3")
    pr("jmp Object.copy.while")


    Utilities.output += "Object.copy.whileEnd:\n"
    pr("mov r1 <- r0")
    ret(racc)

    log("out_string")
    Utilities.output += "IO.out_string:\n"
    callee_init()
    pr("ld %s <- fp[3]" % racc)
    pr("ld r1 <- r1[%d]" % attributes_offset)
    pr("syscall IO.out_string")
    pr("mov r1 <- r0")
    ret(racc)

    log("out_int")
    Utilities.output += "IO.out_int:\n"
    callee_init()
    pr("ld %s <- fp[3]" % racc)
    pr("ld r1 <- r1[%d]" % attributes_offset)
    pr("syscall IO.out_int")
    pr("mov r1 <- r0")
    ret(racc)

    log("in_string")
    Utilities.output += "IO.in_string:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "String"))
    new_loc = new.cgen("IO", imp_map, {})
    pr("mov r2 <- r1")
    pr("syscall IO.in_string")
    pr("st r2[%d] <- r1" % attributes_offset)
    pr("mov r1 <- r2")
    ret(racc)

    log("in_int")
    Utilities.output += "IO.in_int:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "Int"))
    new_loc = new.cgen("IO", imp_map, {})
    pr("mov r2 <- r1")
    pr("syscall IO.in_int")
    pr("st r2[%d] <- r1" % attributes_offset)
    pr("mov r1 <- r2")
    ret(racc)

    log("length")
    Utilities.output += "String.length:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "Int"))
    new_loc = new.cgen("String", imp_map, {})
    pr("mov r3 <- r1")
    pr("ld r1 <- r0[%d]" % attributes_offset)
    pr("syscall String.length")
    pr("st r3[%d] <- r1" % attributes_offset)
    pr("mov r1 <- r3")
    ret(racc)

    log("concat")
    Utilities.output += "String.concat:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "String"))
    new_loc = new.cgen("String", imp_map, {})
    pr("mov r3 <- r1")
    pr("mov r1 <- r0")

    pr("ld r2 <- fp[3]")
    pr("syscall String.concat")
    pr("st r3[%d] <- r1" % attributes_offset)
    pr("mov r1 <- r3")
    ret(racc)

    log("substr")
    Utilities.output += "String.substr:\n"
    callee_init()
    new = AST.New(0, AST.Identifier(0, "String"))
    new_loc = new.cgen("String", imp_map, {})
    pr("mov r3 <- r1")

    pr("ld r2 <- fp[3]")
    pr("ld r2 <- r2[%d]" % attributes_offset)
    pr("ld r1 <- fp[4]")
    pr("ld r1 <- r1[%d]" % attributes_offset)
    pr("ld r0 <- r0[%d]" % attributes_offset)
    pr("syscall String.substr")
    pr("bnz r1 %s" % "String.substr.validString")

    pr("la r1 <- the.substring.range.string")
    pr("syscall IO.out_string")
    pr("syscall exit")

    Utilities.output += "String.substr.validString:\n"
    pr("st r3[%d] <- r1" % attributes_offset)
    pr("mov r1 <- r3")


    # methods
    new_section("methods", 0)
    for cls in classes:
        if cls in ["Object", "IO", "Int", "String", "Bool"]:
            continue
        for method in imp_map[cls]:
            if method.type_id != cls:
                continue

            Utilities.output += "%s.%s:\n" % (cls, method.name_id)
            callee_init()

            st = {}
            for i, attribute in enumerate(class_map[cls]):
                st[attribute.name_id] = rself.off(attributes_offset + i)

            for i, formal in enumerate(method.formals_list):
                st[formal.name_id] = Utilities.FP(i + 3)

            st["self"] = rself

            val = method.body_exp.cgen(method.type_id, imp_map, st)

            if val is None:
                print("val is None")
                exit(1)


            ret(racc)


    # start
    new_section("start", 0)
    Utilities.output += "start:\n"
    pr("la r2 <- Main..new")
    pr("call r2")
    pr("ld %s <- %s[%d]" % (rtmp, racc, vtable_offset))

    # get main offset from Main vtable
    method_offset = -1
    for i, method in enumerate(imp_map["Main"]):
        if method.name_id == "main":
            method_offset = i + vtable_methods_offset
    if method_offset == -1:
        print("Could not find method")
        exit(1)
    pr("ld %s <- %s[%d]" % (rtmp, rtmp, method_offset))
    pr("push fp")
    pr("push r1")
    pr("call %s" % rtmp)
    pr("syscall exit")

    with open(sys.argv[1][:-4] + "asm", "w+") as f:
        f.write(Utilities.output)

    return




if __name__ == '__main__':
    main()
    exit(0)



