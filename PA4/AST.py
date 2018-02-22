class Class(object):
    name_id = None
    parent_id = None
    features = []

    def __init__(self, _name, _parent, _features):
        self.name_id = _name
        self.parent_id = _parent
        self.features = _features



    def __str__(self):
        to_return = ""
        to_return += str(self.name_id)
        if self.parent_id is None:
            to_return += "no_inherits\n"
        else:
            to_return += "inherits\n" + str(self.parent_id)
        to_return += str(len(self.features)) + "\n"
        for feature in self.features:
            to_return += str(feature)

        return to_return


class Identifier(object):
    lineno = None
    id = None

    def __init__(self, _lineno, _id):
        self.lineno = _lineno
        self.id = _id

    def __str__(self, ):
        return self.lineno + "\n" + self.id + "\n"

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

class Feature(object):
    name_id = None

    def __init__(self, _name):
        self.name_id = _name


class Attribute(Feature):
    type_id = None
    init_exp = None

    def __init__(self, _name, _type, _init):
        Feature.__init__(self, _name)
        self.type_id = _type
        self.init_exp = _init

    def __str__(self):
        to_return = ""

        if self.init_exp is None:
            to_return += "attribute_no_init" + "\n"
        else:
            to_return += "attribute_init" + "\n"

        to_return += str(self.name_id)
        to_return += str(self.type_id)

        if self.init_exp is not None:
            to_return += str(self.init_exp)

        return to_return



class Method(Feature):
    formals_list = []
    type_id = None
    body_exp = None


    def __init__(self, _name, _formals, _type, _body):
        Feature.__init__(self, _name)
        self.formals_list = _formals
        self.type_id = _type
        self.body_exp = _body


    def __str__(self):
        to_return = "method\n" + str(self.name_id)
        to_return += str(len(self.formals_list)) + "\n"

        for formal in self.formals_list:
            to_return += str(formal)
        to_return += str(self.type_id)
        to_return += str(self.body_exp)
        return to_return


class Formal(object):
    name_id = None
    type_id = None

    def __init__(self, _name, _type):
        self.name_id = _name
        self.type_id = _type

    def __str__(self):
        return str(self.name_id) + str(self.type_id)

    def __eq__(self, other):
        return self.type_id == other.type_id


class Expression(object):
    lineno = None
    exp_name = "INSTANCE OF EXPRESSION"
    exp_type = None

    def __init__(self, _lineno):
        self.lineno = _lineno

    def __str__(self):
        return self.lineno + "\n" + str(self.exp_type) + "\n" + self.exp_name + "\n"

    def find_type(self, _i, types, cl):
        if _i.id == "self":
            return "SELF_TYPE"
        for i, t in types:
            if i == _i.id:
                return t
        return None

    def is_parent_of(self, parent_id, cl_id, ast, cl):


        if parent_id is None:
            return True
        if cl_id is None:
            return False

        if parent_id.id == "SELF_TYPE":
            parent_id = cl
        if cl_id.id == "SELF_TYPE":
            cl_id = cl

        if cl_id == parent_id:
            return True

        curr_class = None
        for cl in ast:
            if cl.name_id == cl_id:
                curr_class = cl
                break
        return self.is_parent_of(parent_id, curr_class.parent_id, ast, cl)

    def mutual_parent(self, cl1_id, cl2_id, ast, cl):

        if cl1_id is None or cl2_id is None:
            for cl in ast:
                if cl.name_id == "Object":
                    return cl.name_id

        if cl1_id.id == "SELF_TYPE":
            cl1_id = cl
        if cl2_id.id == "SELF_TYPE":
            cl2_id = cl

        if self.is_parent_of(cl1_id, cl2_id, ast, cl):
            return cl1_id
        cl1_class = None
        for cl in ast:
            if cl.name_id == cl1_id:
                cl1_class = cl
                break
        return self.mutual_parent(cl1_class.parent_id, cl2_id, ast, cl)

    def find_class(self, ast, id):
        if id is None:
            return None
        for cl in ast:
            if cl.name_id == id:
                return cl

    def find_origin_class(self, ast, curr, method_id):

        if curr is None:
            object_class = None
            for pred in ast:
                if pred.name_id.id == "Object":
                    object_class = pred
                    break
            return object_class.name_id

        cl = self.find_class(ast, curr)
        for feature in cl.features:
            if not isinstance(feature, Method):
                continue
            if feature.name_id == method_id:
                return cl.name_id
        return self.find_origin_class(ast, cl.parent_id, method_id)



    def get_type(self, cl, M, O, ast):
        return None



class Assign(Expression):
    var_id = None
    rhs_exp = None

    def __init__(self, _lineno, _var, _rhs):
        Expression.__init__(self, _lineno)
        self.exp_name = "assign"
        self.var_id = _var
        self.rhs_exp = _rhs

    def __str__(self):
        return Expression.__str__(self) + str(self.var_id) + str(self.rhs_exp)

    def get_type(self, cl, M, O, ast):
        var_type = self.find_type(self.var_id, O, cl)
        rhs_type = self.rhs_exp.get_type(cl, M, O, ast)
        if not self.is_parent_of(Identifier(0, var_type), Identifier(0, rhs_type), ast, cl):
            print("ERROR: " + self.lineno +
                  ": Type-Check: assign no conform " + self.var_id.id)
            exit(1)
        self.exp_type = rhs_type
        return self.exp_type





class Dynamic_Dispatch(Expression):
    e_exp = None
    method_id = None
    args_exp_list = []

    def __init__(self, _lineno, _e, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "dynamic_dispatch"
        self.e_exp = _e
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):
        to_return = Expression.__str__(self) + str(self.e_exp) + str(self.method_id)
        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        lhs_type = self.e_exp.get_type(cl, M, O, ast)
        if lhs_type == "SELF_TYPE":
            lhs_type = cl.id

        formals = []
        original = self.find_class(ast, self.find_origin_class(ast, Identifier(0, lhs_type), self.method_id))
        for feature in original.features:
            if not isinstance(feature, Method):
                continue
            if feature.name_id == self.method_id:
                formals += feature.formals_list
                self.exp_type = feature.type_id.id
                break

        for i, exp in enumerate(self.args_exp_list):
            type = exp.get_type(cl, M, O, ast)

            exp_type_id = Identifier(0, type)
            if not self.is_parent_of(formals[i].type_id, exp_type_id, ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: does not match formals ")
                exit(1)


        return self.exp_type



class Static_Dispatch(Expression):
    e_exp = None
    type_id = None
    method_id = None
    args_exp_list = []

    def __init__(self, _lineno, _e, _type, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "static_dispatch"
        self.e_exp = _e
        self.type_id = _type
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):
        to_return = Expression.__str__(self) + str(self.e_exp) + str(self.type_id) + str(self.method_id)
        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        lhs_type = self.e_exp.get_type(cl, M, O, ast)
        if lhs_type == "SELF_TYPE":
            lhs_type = cl.id
        lhs_type = self.type_id.id
        formals = []
        original = self.find_class(ast, self.find_origin_class(ast, Identifier(0, lhs_type), self.method_id))
        for feature in original.features:
            if not isinstance(feature, Method):
                continue
            if feature.name_id == self.method_id:
                formals += feature.formals_list
                self.exp_type = feature.type_id.id
                break

        for i, exp in enumerate(self.args_exp_list):
            type = exp.get_type(cl, M, O, ast)

            exp_type_id = Identifier(0, type)
            if not self.is_parent_of(formals[i].type_id, exp_type_id, ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: does not match formals ")
                exit(1)

        return self.exp_type


class Self_Dispatch(Expression):
    method_id = None
    args_exp_list = []

    def __init__(self, _lineno, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "self_dispatch"
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):
        to_return = Expression.__str__(self) + str(self.method_id)
        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def get_type(self, cl, M, O, ast):

        lhs_type = cl.id

        formals = []
        original = self.find_class(ast, self.find_origin_class(ast, Identifier(0, lhs_type), self.method_id))
        for feature in original.features:
            if not isinstance(feature, Method):
                continue
            if feature.name_id == self.method_id:
                formals += feature.formals_list
                self.exp_type = feature.type_id.id
                break

        for i, exp in enumerate(self.args_exp_list):
            type = exp.get_type(cl, M, O, ast)

            exp_type_id = Identifier(0, type)
            if not self.is_parent_of(formals[i].type_id, exp_type_id, ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: does not match formals ")
                exit(1)

        return self.exp_type

class If(Expression):
    pred_exp = None
    then_exp = None
    else_exp = None

    def __init__(self, _lineno, _pred, _then, _else):
        Expression.__init__(self, _lineno)
        self.exp_name = "if"
        self.pred_exp = _pred
        self.then_exp = _then
        self.else_exp = _else

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.pred_exp)
        to_return += str(self.then_exp)
        to_return += str(self.else_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        pred_type = self.pred_exp.get_type(cl, M, O, ast)
        then_type = self.then_exp.get_type(cl, M, O, ast)
        else_type = self.else_exp.get_type(cl, M, O, ast)
        if pred_type != "Bool":
            print("ERROR: " + self.lineno +
                  ": Type-Check: predicate not of type Bool ")
            exit(1)
        self.exp_type = self.mutual_parent(Identifier(0, then_type), Identifier(0, else_type), ast, cl).id

        return self.exp_type


class While(Expression):
    pred_exp = None
    body_exp = None


    def __init__(self, _lineno, _pred, _body):
        Expression.__init__(self, _lineno)
        self.exp_name = "while"
        self.pred_exp = _pred
        self.body_exp = _body

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.pred_exp)
        to_return += str(self.body_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        pred_type = self.pred_exp.get_type(cl, M, O, ast)
        body_type = self.body_exp.get_type(cl, M, O, ast)

        if pred_type != "Bool":
            print("ERROR: " + self.lineno +
                  ": Type-Check: predicate not of type Bool ")
            exit(1)

        self.exp_type = "Object"
        return self.exp_type


class Block(Expression):
    body_exp_list = []


    def __init__(self, _lineno, _body):
        Expression.__init__(self, _lineno)
        self.exp_name = "block"
        self.body_exp_list = _body

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(len(self.body_exp_list)) + "\n"
        for exp in self.body_exp_list:
            to_return += str(exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        for exp in self.body_exp_list:
            e_type = exp.get_type(cl, M, O, ast)
        self.exp_type = self.body_exp_list[-1].get_type(cl, M, O, ast)
        return self.exp_type


class New(Expression):
    class_id = None

    def __init__(self, _lineno, _class):
        Expression.__init__(self, _lineno)
        self.exp_name = "new"
        self.class_id = _class

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.class_id)
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = self.class_id.id
        return self.exp_type


class Isvoid(Expression):
    e_exp = None

    def __init__(self, _lineno, _e):
        Expression.__init__(self, _lineno)
        self.exp_name = "isvoid"
        self.e_exp = _e

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.e_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        e_type = self.e_exp.get_type()
        self.exp_type = "Bool"
        return self.exp_type


class Plus(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "plus"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)

        if x_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: lhs not Int ")
            exit(1)
        if y_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: rhs not Int ")
            exit(1)


        self.exp_type = "Int"
        return self.exp_type


class Minus(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "minus"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)

        if x_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: lhs not Int ")
            exit(1)
        if y_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: rhs not Int ")
            exit(1)

        self.exp_type = "Int"
        return self.exp_type


class Times(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "times"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)


        if x_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: lhs not Int ")
            exit(1)
        if y_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: rhs not Int ")
            exit(1)

        self.exp_type = "Int"
        return self.exp_type


class Divide(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "divide"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)

        if x_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: lhs not Int ")
            exit(1)
        if y_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: rhs not Int ")
            exit(1)


        self.exp_type = "Int"
        return self.exp_type


class Lt(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "lt"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)

        allowed = ["Int", "String", "Bool"]

        if x_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)
        if y_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)


        self.exp_type = "Bool"
        return self.exp_type

class Le(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "le"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)
        self.exp_type = "Bool"

        allowed = ["Int", "String", "Bool"]

        if x_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)
        if y_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)

        return self.exp_type


class Eq(Expression):
    x_exp = None
    y_exp = None

    def __init__(self, _lineno, _x, _y):
        Expression.__init__(self, _lineno)
        self.exp_name = "eq"
        self.x_exp = _x
        self.y_exp = _y

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        to_return += str(self.y_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)
        y_type = self.y_exp.get_type(cl, M, O, ast)

        allowed = ["Int", "String", "Bool"]

        if x_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)
        if y_type in allowed and x_type != y_type:
            print("ERROR: " + self.lineno +
                  ": Type-Check: only allowed to compare primitives to same class ")
            exit(1)

        self.exp_type = "Bool"
        return self.exp_type


class Not(Expression):
    x_exp = None

    def __init__(self, _lineno, _x):
        Expression.__init__(self, _lineno)
        self.exp_name = "not"
        self.x_exp = _x

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)

        if x_type != "Bool":
            print("ERROR: " + self.lineno +
                  ": Type-Check: can only not Bool ")
            exit(1)

        self.exp_type = "Bool"
        return self.exp_type

class Negate(Expression):
    x_exp = None

    def __init__(self, _lineno, _x):
        Expression.__init__(self, _lineno)
        self.exp_name = "negate"
        self.x_exp = _x

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.x_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        x_type = self.x_exp.get_type(cl, M, O, ast)

        if x_type != "Int":
            print("ERROR: " + self.lineno +
                  ": Type-Check: can only negate Int ")
            exit(1)

        self.exp_type = "Int"
        return self.exp_type

class Integer(Expression):
    int_const = None

    def __init__(self, _lineno, _int):
        Expression.__init__(self, _lineno)
        self.exp_name = "integer"
        self.int_const = _int

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.int_const) + "\n"
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = "Int"
        return self.exp_type


class String(Expression):
    str_const = None

    def __init__(self, _lineno, _str):
        Expression.__init__(self, _lineno)
        self.exp_name = "string"
        self.str_const = _str

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.str_const) + "\n"
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = "String"
        return self.exp_type


class Identifier_Exp(Expression):
    var_id = None

    def __init__(self, _lineno, _var):
        Expression.__init__(self, _lineno)
        self.exp_name = "identifier"
        self.var_id = _var

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.var_id)
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = self.find_type(self.var_id, O, cl)
        return self.exp_type

class True_Exp(Expression):
    def __init__(self, _lineno):
        Expression.__init__(self, _lineno)
        self.exp_name = "true"

    def __str__(self):
        to_return = Expression.__str__(self)
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = "Bool"
        return self.exp_type

class False_Exp(Expression):
    def __init__(self, _lineno):
        Expression.__init__(self, _lineno)
        self.exp_name = "false"

    def __str__(self):
        to_return = Expression.__str__(self)
        return to_return

    def get_type(self, cl, M, O, ast):
        self.exp_type = "Bool"
        return self.exp_type


class Let(Expression):
    binding_list = []
    body_exp = None

    def __init__(self, _lineno, _binding_list, _body):
        Expression.__init__(self, _lineno)
        self.exp_name = "let"
        self.binding_list = _binding_list
        self.body_exp = _body

    def __str__(self):
        to_return = Expression.__str__(self) + str(len(self.binding_list)) + "\n"
        for binding in self.binding_list:
            to_return += str(binding)
        to_return += str(self.body_exp)
        return to_return

    def get_type(self, cl, M, O, ast):
        additional_O = []
        for binding in self.binding_list:
            additional_O.append((binding.var_id.id, binding.type_id.id))
            type = binding.value_exp.get_type(cl, M, O, ast)

            if type is not None and not self.is_parent_of(binding.type_id, Identifier(0, type), ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: types don't match in let ")
                exit(1)


        self.exp_type = self.body_exp.get_type(cl, M,additional_O + O , ast)
        return self.exp_type

class Binding(object):
    var_id = None
    type_id = None
    value_exp = None

    def __init__(self, _var, _type, _value):
        self.var_id = _var
        self.type_id = _type
        self.value_exp = _value

    def __str__(self):
        to_return = ""
        if self.value_exp is None:
            to_return += "let_binding_no_init\n"
        else:
            to_return += "let_binding_init\n"
        to_return += str(self.var_id) + str(self.type_id)
        if self.value_exp is not None:
            to_return += str(self.value_exp)
        return to_return


class Case(Expression):
    case_exp = None
    case_elem_list = []

    def __init__(self, _lineno, _case, _case_elem_list):
        Expression.__init__(self, _lineno)
        self.exp_name = "case"
        self.case_exp = _case
        self.case_elem_list = _case_elem_list

    def __str__(self):
        to_return = Expression.__str__(self) + str(self.case_exp) + str(len(self.case_elem_list)) + "\n"
        for case_elem in self.case_elem_list:
            to_return += str(case_elem)
        return to_return

    def get_type(self, cl, M, O, ast):
        exp_type = self.case_exp.get_type(cl, M, O, ast)
        for elem in self.case_elem_list:
            elem_type = elem.body_exp.get_type(cl, M, O, ast)

            if elem_type is not None and not self.is_parent_of(elem.type_id, Identifier(0, elem_type), ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: types don't match in case ")
                exit(1)

            if elem.type_id.id == exp_type:
                self.exp_type = elem_type

        if self.exp_type is None:
            self.exp_type = "Object"

        return self.exp_type


class Case_Elem(object):
    var_id = None
    type_id = None
    body_exp = None

    def __init__(self, _var, _type, _body):
        self.var_id = _var
        self.type_id = _type
        self.body_exp = _body

    def __str__(self):
        return str(self.var_id) + str(self.type_id) + str(self.body_exp)