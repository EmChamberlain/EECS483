import sys
import AST
from Toposort import toposort




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


def get_predefined_classes():
    to_return = []

    name = AST.Identifier(0, "Object")
    parent = None
    features = []
    features.append(AST.Method(AST.Identifier(0, "abort"), [], AST.Identifier(0, "Object"), None))
    features.append(AST.Method(AST.Identifier(0, "copy"), [], AST.Identifier(0, "SELF_TYPE"), None))
    features.append(AST.Method(AST.Identifier(0, "type_name"), [], AST.Identifier(0, "String"), None))
    to_return.append(AST.Class(name, parent, features))

    name = AST.Identifier(0, "IO")
    parent = AST.Identifier(0, "Object")
    features = []

    features.append(AST.Method(AST.Identifier(0, "in_int"), [], AST.Identifier(0, "Int"), None))

    features.append(AST.Method(AST.Identifier(0, "in_string"), [], AST.Identifier(0, "String"), None))


    features.append(AST.Method(AST.Identifier(0, "out_int"),
                               [AST.Formal(AST.Identifier(0, "x"), AST.Identifier(0, "Int"))],
                               AST.Identifier(0, "SELF_TYPE"), None))

    features.append(AST.Method(AST.Identifier(0, "out_string"),
                               [AST.Formal(AST.Identifier(0, "x"), AST.Identifier(0, "String"))],
                               AST.Identifier(0, "SELF_TYPE"), None))
    to_return.append(AST.Class(name, parent, features))

    name = AST.Identifier(0, "Int")
    parent = AST.Identifier(0, "Object")
    features = []
    to_return.append(AST.Class(name, parent, features))

    name = AST.Identifier(0, "String")
    parent = AST.Identifier(0, "Object")
    features = []
    features.append(AST.Method(AST.Identifier(0, "concat"),
                               [AST.Formal(AST.Identifier(0, "s"), AST.Identifier(0, "String"))],
                               AST.Identifier(0, "String"), None))

    features.append(AST.Method(AST.Identifier(0, "length"), [], AST.Identifier(0, "Int"), None))

    features.append(AST.Method(AST.Identifier(0, "substr"),
                               [AST.Formal(AST.Identifier(0, "i"), AST.Identifier(0, "Int")),
                                AST.Formal(AST.Identifier(0, "l"), AST.Identifier(0, "Int"))],
                               AST.Identifier(0, "String"), None))
    to_return.append(AST.Class(name, parent, features))

    name = AST.Identifier(0, "Bool")
    parent = AST.Identifier(0, "Object")
    features = []
    to_return.append(AST.Class(name, parent, features))

    return to_return

def class_map_key(cl):
    if isinstance(cl, str):
        return cl
    return cl.name_id.id

def features_key(attri):
    return attri.name_id.id


def find_class(ast, id):
    if id is None:
        return None
    for cl in ast:
        if cl.name_id == id:
            return cl



def get_features(ast, cl):
    if cl.parent_id is None:
        return cl.features
    if cl.name_id.id in ["Bool", "IO", "Int", "Object", "String"]:
        return cl.features

    parent_class = find_class(ast, cl.parent_id)
    return get_features(ast, parent_class) + cl.features


def get_class_map(ast):
    to_return = "class_map\n"
    to_return += str(len(ast)) + "\n"
    for cl in sorted(ast, key=class_map_key):
        to_return += cl.name_id.id + "\n"
        attributes = []
        features = get_features(ast, cl)
        for feature in features:
            if isinstance(feature, AST.Attribute):
                attributes.append(feature)
        to_return += str(len(attributes)) + "\n"
        for attri in attributes:
            if attri.init_exp is None:
                to_return += "no_initializer\n"
            else:
                to_return += "initializer\n"
            to_return += str(attri.name_id.id) + "\n" + str(attri.type_id.id) + "\n"
            if attri.init_exp is not None:
                to_return += str(attri.init_exp)
    return to_return

def find_origin_class(ast, curr, prev, method):

    if curr is None:
        return prev
    cl = find_class(ast, curr)
    for feature in cl.features:
        if not isinstance(feature, AST.Method):
                continue
        if feature.name_id == method.name_id:
            return find_origin_class(ast, cl.parent_id, curr, method)
    return prev

def get_idents_types(ast, cl, method):
    to_return = []
    for feature in get_features(ast, cl):
        if not isinstance(feature, AST.Attribute):
            continue
        to_return.append((feature.name_id, feature.type_id))
    for formal in method.formal_list:
        to_return.append((formal.name_id, formal.type_id))
    return to_return

def get_check_body_expression(exp, idents_types):
    exp.get_type()


def get_implementation_map(ast, predefined_classes):
    predefined_classes_str = ["Bool", "IO", "Int", "Object", "String"]
    to_return = "implementation_map\n"
    to_return += str(len(ast) + len(predefined_classes)) + "\n"
    for cl in sorted(ast + predefined_classes, key=class_map_key):
        to_return += cl.name.id + "\n"
        methods = []
        for feature in get_features(ast + predefined_classes, cl.features):
            if not isinstance(feature, AST.Method):
                continue
            methods.append(feature)

        to_return += str(len(methods)) + "\n"
        for method in methods:
            to_return += method.name_id.id + "\n"
            to_return += str(len(method.formals_list)) + "\n"
            for formal in method.formals_list:
                to_return += formal.name_id.id + "\n"
            origin_class_id = find_origin_class(ast, cl.parent_id, cl.name_id, method)
            # origin_class = find_class(ast, origin_class_id)
            to_return += origin_class_id.id + "\n"
            if origin_class_id.id in predefined_classes_str:
                to_return += str(0) + "\n"
                to_return += method.type_id.id + "\n"
                to_return += "internal\n"
                to_return += origin_class_id.id + "." + method.name_id.id + "\n"
            else:
                idents_types = get_idents_types(ast + predefined_classes, cl, method)
                body_type_id, exp_name = get_check_body_expression(method.body_exp, idents_types)
                to_return += method.body_exp.lineno + "\n"
                to_return += body_type_id.id + "\n"
                to_return += exp_name + "\n"


def check_class_map(ast, predefined_classes):

    predefined_names = ["Bool", "IO", "Int", "Object", "String"]

    # redefined predefined
    for cl in ast:
        if cl.name_id.id in predefined_names:
            print("ERROR: " + cl.name_id.lineno +
                  ": Type-Check: redefined predefined " + cl.name_id.id)
            exit(1)


    can_inherit_list = ["Object", "IO"]
    parent_edges = []

    for cl in ast:
        can_inherit_list.append(cl.name_id.id)
        if cl.parent_id is None:
            parent_edges.append((cl.name_id.id, "Object"))
            continue
        parent_edges.append((cl.name_id.id, cl.parent_id.id))

    # bad inherit
    for cl in ast:
        if cl.parent_id is None:
            continue
        if cl.name_id == cl.parent_id:
            print("ERROR: " + cl.parent_id.lineno + ": Type-Check: cannot inherit from self" + cl.parent_id.id)
            exit(1)
        if cl.parent_id.id not in can_inherit_list:
            print("ERROR: " + cl.parent_id.lineno + ": Type-Check: cannot inherit from " + cl.parent_id.id)
            exit(1)

    # cycle
    topo, valid = toposort(parent_edges)
    if not valid:
        print("ERROR: 0: Type-Check: Cycle")
        exit(1)


    # multiple feature definitions
    for cl in ast:
        for i, feature1 in enumerate(cl.features):
            for j, feature2 in enumerate(cl.features[i+1:]):
                if (feature1.name_id == feature2.name_id) and (i != j):
                    if isinstance(feature1, AST.Method) == isinstance(feature2.AST.Method):
                        print("ERROR: " + feature2.name_id.lineno +
                              ": Type-Check: multiple definitions of " + feature2.name_id.id)
                        exit(1)

    # redefining parameters of parent
    for cl in ast:
        parent_class = find_class(ast + predefined_classes, cl.parent_id)
        while parent_class is not None:
            for feature1 in cl.features:
                for feature2 in parent_class.features:
                    if not isinstance(feature1, AST.Method):
                        continue
                    if not isinstance(feature2, AST.Method):
                        continue
                    if feature1.name_id == feature2.name_id:
                        #TODO: Fix this if failing tests
                        if feature1.formals_list != feature2.formals_list:
                            if len(feature1.formals_list) == 0:
                                print("ERROR: " + feature1.name_id.lineno +
                                      ": changes number of formals " + feature1.name_id.id)
                                exit(1)
                            print("ERROR: " + feature1.formals_list[0].name_id.lineno +
                                  ": Type-Check: parameters don't match " + feature1.formals_list[0].name_id.id)
                            exit(1)
                        if feature1.type_id != feature2.type_id:
                            print("ERROR: " + feature1.type_id.lineno +
                                  ": Type-Check: return type doesn't match " + feature1.type_id.id)
                            exit(1)
            parent_class = find_class(ast + predefined_classes, parent_class.parent_id)

        object_class = None
        for pred in predefined_classes:
            if pred.name_id.id == "Object":
                object_class = pred
                break
        for feature1 in cl.features:
            for feature2 in object_class.features:
                if not isinstance(feature1, AST.Method):
                    continue
                if not isinstance(feature2, AST.Method):
                    continue
                if feature1.name_id == feature2.name_id:
                    if feature1.formals_list != feature2.formals_list:
                        if len(feature1.formals_list) == 0:
                            print("ERROR: " + feature1.name_id.lineno +
                                  ": changes number of formals " + feature1.name_id.id)
                            exit(1)
                        print("ERROR: " + feature1.formals_list[0].name_id.lineno +
                              ": Type-Check: parameters don't match " + feature1.formals_list[0].name_id.id)
                        exit(1)
                    if feature1.type_id != feature2.type_id:
                        print("ERROR: " + feature1.type_id.lineno +
                              ": Type-Check: return type doesn't match " + feature1.type_id.id)
                        exit(1)

    # no Main
    found_main = False
    for cl in ast:
        if cl.name_id.id == "Main":
            found_main = True
            break
    if not found_main:
        print("ERROR: " + str(0) +
              ": Type-Check: cannot find class Main " + feature1.type_id.id)
        exit(1)


    # no main in Main
    for cl in ast:
        if cl.name_id.id == "Main":
            method_list = []
            for feature in cl.features:
                if not isinstance(feature, AST.Method):
                    continue
                method_list.append(feature.name_id.id)
            if "main" not in method_list:
                print("ERROR: " + str(0) +
                      ": Type-Check: no main method " + cl.name_id.id)
                exit(1)

    for cl in ast:
        if cl.name_id.id == "Main":
            for feature in cl.features:
                if not isinstance(feature, AST.Method):
                    continue
                if feature.name_id.id == "main":
                    if len(feature.formals_list) != 0:
                        print("ERROR: " + str(0) +
                              ": Type-Check: main has formals ")
                        exit(1)
                    break

    # duplicate formals
    for cl in ast:
        for feature in cl.features:
            if not isinstance(feature, AST.Method):
                continue
            for i, formal1 in enumerate(feature.formals_list):
                for j, formal2 in enumerate(feature.formals_list[i+1:]):
                    if formal1.name_id == formal2.name_id:
                        print("ERROR: " + formal2.name_id.lineno +
                              ": Type-Check: duplicate formals " + formal2.name_id.id)
                        exit(1)


    # attribute named self
    for cl in ast:
        for feature in cl.features:
            if not isinstance(feature, AST.Attribute):
                continue
            if feature.name_id.id == "self":
                print("ERROR: " + feature.name_id.lineno +
                      ": Type-Check: attribute named self " + feature.name_id.id)
                exit(1)

    # override attribute
    for cl in ast:
        parent_class = find_class(ast + predefined_classes, cl.parent_id)
        while parent_class is not None:
            for feature1 in cl.features:
                for feature2 in parent_class.features:
                    if not isinstance(feature1, AST.Attribute):
                        continue
                    if not isinstance(feature2, AST.Attribute):
                        continue
                    if feature1.name_id == feature2.name_id:
                        print("ERROR: " + feature1.name_id.lineno +
                              ": Type-Check: override attribute " + feature1.name_id.id)
                        exit(1)
            parent_class = find_class(ast + predefined_classes, parent_class.parent_id)

    # redefined another class
    for i, cl1 in enumerate(ast):
        for j, cl2 in enumerate(ast[i+1:]):
            if cl1.name_id == cl2.name_id:
                print("ERROR: " + cl2.name_id.lineno +
                      ": Type-Check: redefined another class " + cl2.name_id.id)
                exit(1)
    # TODO: Fix this it is causing good cases to fail
    """
    # return an undefined type
    defined_types = ["Bool", "IO", "Int", "Object", "String"]
    for cl in ast:
        defined_types.append(cl.name_id.id)
    for cl in ast:
        for feature in cl.features:
            if not isinstance(feature, AST.Method):
                continue
            if feature.type_id.id not in defined_types:
                print("ERROR: " + feature.type_id.lineno +
                      ": Type-Check: returning undefined type " + feature.type_id.id)
                exit(1)
    """
    # SELF_TYPE redeclared
    for cl in ast:
        for feature in cl.features:
            if not isinstance(feature, AST.Attribute):
                continue
            if feature.name_id.id == "SELF_TYPE":
                print("ERROR: " + feature.name_id.lineno +
                      ": Type-Check: redefined SELF_TYPE " + feature.name_id.id)
                exit(1)

    # self/SELF_TYPE in formal
    for cl in ast:
        for feature in cl.features:
            if not isinstance(feature, AST.Method):
                continue
            for formal in feature.formals_list:
                if formal.name_id.id == "self":
                    print("ERROR: " + formal.name_id.lineno +
                          ": Type-Check: self in formal " + formal.name_id.id)
                    exit(1)
                if formal.type_id.id == "SELF_TYPE":
                    print("ERROR: " + formal.type_id.lineno +
                          ": Type-Check: SELF_TYPE in formal " + formal.type_id.id)
                    exit(1)





with open(sys.argv[1], 'r') as f:
    in_lines = [l.rstrip('\r\n') for l in f.readlines()]

ast = get_ast()
predefined_classes = get_predefined_classes()

check_class_map(ast, predefined_classes)


out_string = get_class_map(ast + predefined_classes)


file_name = sys.argv[1][:-3] + "type"

with open(file_name, 'w+') as f:
    f.write(out_string)


