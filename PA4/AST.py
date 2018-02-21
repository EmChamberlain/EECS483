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
        return self.lineno + "\n" + self.exp_type + "\n" + self.exp_name + "\n"

    def find_type(self, _i, types):
        for i, t in types:
            if i == _i.id:
                return t
        return None

    def get_type(self, cl, M, O):
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

    def get_type(self, cl, M, O):
        self.exp_type = self.rhs_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        pred_bool = self.pred_exp.get_type(cl, M, O)
        if isinstance(pred_bool, True_Exp):
            self.exp_type = self.then_exp.get_type(cl, M, O)
        else:
            self.exp_type = self.else_exp.get_type(cl, M, O)

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

    def get_type(self, cl, M, O):
        pred_type = self.pred_exp.get_type(cl, M, O)
        body_type = self.pred_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        for exp in self.body_exp_list:
            e_type = exp.get_type(cl, M, O)
        self.exp_type = self.body_exp_list[-1].get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
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

    def get_type(self, cl, M, O):
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
        self.exp_type = "Bool"
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
        y_type = self.y_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
        x_type = self.x_exp.get_type(cl, M, O)
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

    def get_type(self, cl, M, O):
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

    def get_type(self, cl, M, O):
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

    def get_type(self, cl, M, O):
        self.exp_type = self.find_type(self.var_id, O)
        return self.exp_type

class True_Exp(Expression):
    def __init__(self, _lineno):
        Expression.__init__(self, _lineno)
        self.exp_name = "true"

    def __str__(self):
        to_return = Expression.__str__(self)
        return to_return

    def get_type(self, cl, M, O):
        self.exp_type = "Bool"
        return self.exp_type

class False_Exp(Expression):
    def __init__(self, _lineno):
        Expression.__init__(self, _lineno)
        self.exp_name = "false"

    def __str__(self):
        to_return = Expression.__str__(self)
        return to_return

    def get_type(self, cl, M, O):
        self.exp_type = "Bool"
        return self.exp_type


class Let(Expression):
    binding_list = []
    body_exp = None

    def __init__(self, _lineno, _binding_list, _body):
        self.lineno = _lineno
        self.exp_name = "let"
        self.binding_list = _binding_list
        self.body_exp = _body

    def __str__(self):
        to_return = Expression.__str__(self) + str(len(self.binding_list)) + "\n"
        for binding in self.binding_list:
            to_return += str(binding)
        to_return += str(self.body_exp)
        return to_return

    def get_type(self, cl, M, O):
        new_ids = []
        for binding in self.binding_list:
            new_ids.append((binding.var_id.id, binding.type_id.id))
            type = binding.value_exp.get_type(cl, M, O)

        self.exp_type = self.body_exp.get_type(cl, M, O + new_ids)
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
        self.lineno = _lineno
        self.exp_name = "case"
        self.case_exp = _case
        self.case_elem_list = _case_elem_list

    def __str__(self):
        to_return = Expression.__str__(self) + str(self.case_exp) + str(len(self.case_elem_list)) + "\n"
        for case_elem in self.case_elem_list:
            to_return += str(case_elem)
        return to_return


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