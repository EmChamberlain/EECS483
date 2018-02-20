import sys
import AST




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
        val = get_expression()
    return AST.Binding(var, type, val)

def get_case_elem():
    var = get_identifier()
    type = get_identifier()
    body = get_expression()
    return AST.Case_Elem(var, type, body)

def get_expression():
    lineno = get_line()
    name = get_line()

    if name == "assign":
        var = get_identifier()
        rhs = get_expression()
        return AST.Assign(lineno, var, rhs)
    elif name == "dynamic_dispatch":
        e = get_expression()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_expression())
        return AST.Dynamic_Dispatch(lineno, e, method, args)
    elif name == "static_dispatch":
        e = get_expression()
        type = get_identifier()
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_expression())
        return AST.Static_Dispatch(lineno, e, type, method, args)
    elif name == "self_dispatch":
        method = get_identifier()
        args = []
        num_args = int(get_line())
        for i in range(num_args):
            args.append(get_expression())
        return AST.Self_Dispatch(lineno, method, args)
    elif name == "if":
        pred = get_expression()
        then = get_expression()
        else_exp = get_expression()
        return AST.If(lineno, pred, then, else_exp)
    elif name == "while":
        pred = get_expression()
        body = get_expression()
        return AST.While(lineno, pred, body)
    elif name == "block":
        body_exp_list = []
        num_body_exp = int(get_line())
        for i in range(num_body_exp):
            body_exp_list.append(get_expression())
        return AST.Block(lineno, body_exp_list)
    elif name == "new":
        class_id = get_identifier()
        return AST.New(lineno, class_id)
    elif name == "isvoid":
        e = get_expression()
        return AST.Isvoid(lineno, e)
    elif name == "plus":
        x = get_expression()
        y = get_expression()
        return AST.Plus(lineno, x, y)
    elif name == "minus":
        x = get_expression()
        y = get_expression()
        return AST.Minus(lineno, x, y)
    elif name == "times":
        x = get_expression()
        y = get_expression()
        return AST.Times(lineno, x, y)
    elif name == "divide":
        x = get_expression()
        y = get_expression()
        return AST.Divide(lineno, x, y)
    elif name == "lt":
        x = get_expression()
        y = get_expression()
        return AST.Lt(lineno, x, y)
    elif name == "le":
        x = get_expression()
        y = get_expression()
        return AST.Le(lineno, x, y)
    elif name == "eq":
        x = get_expression()
        y = get_expression()
        return AST.Eq(lineno, x, y)
    elif name == "not":
        x = get_expression()
        return AST.Not(lineno, x)
    elif name == "negate":
        x = get_expression()
        return AST.Negate(lineno, x)
    elif name == "integer":
        int_const = int(get_line())
        return AST.Integer(lineno, int_const)
    elif name == "string":
        str_const = get_line()
        return AST.String(lineno, str_const)
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
        body = get_expression()
        return AST.Let(lineno, bindings, body)
    elif name == "case":
        case_exp = get_expression()
        case_elems = []
        num_elems = int(get_line())
        for i in range(num_elems):
            case_elems.append(get_case_elem())
        return AST.Case(lineno, case_exp, case_elems)
    else:
        print("Expression switch defaulted: " + str(name))
        exit(1)





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
        init = get_expression()
        return AST.Attribute(name, type, init)
    elif feature_str == "method":
        num_formals = int(get_line())

        for i in range(num_formals):
            formals_list.append(get_formal())

        type = get_identifier()
        body = get_expression()
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


def get_ast():
    class_list = []
    num_classes = int(get_line())
    for i in range(num_classes):
        class_list.append(get_class())
    return class_list

def class_map_key(cl):
    if isinstance(cl, str):
        return cl
    return cl.name_id.id

def features_key(attri):
    return attri.name_id.id

def get_class_map(ast):
    predefined_classes = ["Bool", "IO", "Int", "Object", "String"]
    to_return = "class_map\n"
    to_return += str(len(ast) + len(predefined_classes)) + "\n"
    for cl in sorted(ast + predefined_classes, key=class_map_key):
        if cl in predefined_classes:
            to_return += cl + "\n"
            to_return += str(0) + "\n"
            continue
        to_return += cl.name_id.id + "\n"
        attributes = []
        for feature in cl.features:
            if isinstance(feature, AST.Attribute):
                attributes.append(feature)
        attributes.sort(key=features_key)
        to_return += str(len(attributes)) + "\n"
        for attri in attributes:
            if attri.init_exp is None:
                to_return += "no_initializer\n"
            else:
                to_return += "initializer\n"
            to_return += str(attri.name_id.id) + "\n" + str(attri.type_id.id) + "\n"
            # TODO: finish this
            if attri.init_exp is not None:
                to_return += str(attri.init_exp)
    return to_return

def get_implementation_map(ast):
    predefined_classes = ["Bool", "IO", "Int", "Object", "String"]
    to_return = "implementation_map\n"
    to_return += str(len(ast) + len(predefined_classes)) + "\n"
    for cl in sorted(ast + predefined_classes, key=class_map_key):
        to_return += cl.name.id + "\n"
        methods = []
        for feature in cl.features:
            if isinstance(feature, AST.Method):
                methods.append()
        methods.sort(key=features_key)
        to_return += str(len(methods)) + "\n"
        for method in methods:
            pass



with open(sys.argv[1], 'r') as f:
    in_lines = [l.rstrip('\r\n') for l in f.readlines()]

ast = get_ast()

out_string = get_class_map(ast)


file_name = sys.argv[1][:-3] + "type"

with open(file_name, 'w+') as f:
    f.write(out_string)


