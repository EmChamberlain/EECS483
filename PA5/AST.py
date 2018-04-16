import Utilities
from Utilities import pr as pr
from Utilities import log as log
from Utilities import call as call
from Utilities import callee_init as callee_init
from Utilities import ret as ret
from Utilities import new_section as new_section


rself = Utilities.rself
racc = Utilities.racc
rtmp = Utilities.rtmp

vtable_object_offset = Utilities.vtable_object_offset
vtable_new_offset = Utilities.vtable_new_offset
vtable_methods_offset = Utilities.vtable_methods_offset

vtable_offset = Utilities.vtable_offset
size_offset = Utilities.size_offset
attributes_offset = Utilities.attributes_offset



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

# base expression class, should never be made directly
class Expression(object):
    lineno = None
    exp_name = "INSTANCE OF EXPRESSION"
    exp_type = None

    def __init__(self, _lineno):
        self.lineno = _lineno

    def __str__(self):
        return self.lineno + "\n" + str(self.exp_type) + "\n" + self.exp_name + "\n"

    # boilerplate for the recursive generation of asm
    def cgen(self, ro, imp_map, st):
        return None

    # find a type in either M or O
    def find_type(self, _i, types, cl):
        if _i.id == "self":
            return "SELF_TYPE"
        for i, t in types:
            if i == _i.id:
                return t
        return None
    # checks is parent_id is a parent of cl_id
    def is_parent_of(self, parent_id, cl_id, ast, cl):


        if parent_id is None:
            return True
        if cl_id is None:
            return False

        if parent_id.id == "SELF_TYPE" and cl_id.id == "SELF_TYPE":
            return parent_id

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
    # returns cl1_id and cl2_id's closest mutual parent
    def mutual_parent(self, cl1_id, cl2_id, ast, cl):

        if cl1_id is None or cl2_id is None:
            for pred in ast:
                if pred.name_id.id == "Object":
                    return pred.name_id

        if cl1_id.id == "SELF_TYPE" and cl2_id.id == "SELF_TYPE":
            return cl1_id

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
    # returns a class based on id
    def find_class(self, ast, id):
        if id is None:
            return None
        for cl in ast:
            if cl.name_id == id:
                return cl

    # returns the first class that has method with id method_id
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


    # the boilerplate for recursively typechecking expressions
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

    def cgen(self, ro, imp_map, st):
        rhs_loc = self.rhs_exp.cgen(ro, imp_map, st)
        v_loc = st[self.var_id.id]
        pr("st %s <- %s" % (v_loc, rhs_loc))

        return rhs_loc

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
    to_print = None


    def __init__(self, _lineno, _e, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "dynamic_dispatch"
        self.e_exp = _e
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):

        temp = self.exp_type
        if self.to_print is not None:
            self.exp_type = self.to_print

        to_return = Expression.__str__(self) + str(self.e_exp) + str(self.method_id)

        self.exp_type = temp

        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def cgen(self, ro, imp_map, st):
        method_offset = -1
        for i, method in enumerate(imp_map[self.exp_type]):
            if method.name_id == self.method_id.id:
                method_offset = i + vtable_methods_offset
        if method_offset == -1:
            print("Could not find method; Dynamic_Dispatch")
            exit(1)
        for i, arg in enumerate(reversed(self.args_exp_list)):
            arg_loc = arg.cgen(ro, imp_map, st)
            pr("push %s" % arg_loc)

        # get vtable pointer
        log("get vtable pointer dynamic")
        pr("la %s <- %s..vtable" % (rtmp, self.exp_type))

        pr("ld %s <- %s[%d]" % (rtmp, rtmp, method_offset))

        call(rtmp)

        for i, arg in enumerate(reversed(self.args_exp_list)):
            pr("pop %s" % rtmp)

        return racc


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

        if self.exp_type == "SELF_TYPE":
            self.exp_type = lhs_type
            # self.to_print = "SELF_TYPE"

        return self.exp_type



class Static_Dispatch(Expression):
    e_exp = None
    type_id = None
    method_id = None
    args_exp_list = []
    to_print = None


    def __init__(self, _lineno, _e, _type, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "static_dispatch"
        self.e_exp = _e
        self.type_id = _type
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):
        temp = self.exp_type
        if self.to_print is not None:
            self.exp_type = self.to_print

        to_return = Expression.__str__(self) + str(self.e_exp) + str(self.type_id) + str(self.method_id)

        self.exp_type = temp

        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def cgen(self, ro, imp_map, st):
        method_offset = -1
        for i, method in enumerate(imp_map[self.type_id.id]):
            if method.name_id == self.method_id.id:
                method_offset = i + vtable_methods_offset
        if method_offset == -1:
            print("Could not find method; Static_Dispatch")
            exit(1)
        for i, arg in enumerate(reversed(self.args_exp_list)):
            arg_loc = arg.cgen(ro, imp_map, st)
            pr("push %s" % arg_loc)

        # get vtable pointer
        log("get vtable pointer static")
        pr("la %s <- %s..vtable" % (rtmp, self.type_id.id))

        pr("ld %s <- %s[%d]" % (rtmp, rtmp, method_offset))

        call(rtmp)

        for i, arg in enumerate(reversed(self.args_exp_list)):
            pr("pop %s" % rtmp)

        return racc

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

        if self.exp_type == "SELF_TYPE":
            self.exp_type = lhs_type
            self.to_print = "SELF_TYPE"

        return self.exp_type


class Self_Dispatch(Expression):
    method_id = None
    args_exp_list = []
    to_print = None

    def __init__(self, _lineno, _method, _args):
        Expression.__init__(self, _lineno)
        self.exp_name = "self_dispatch"
        self.method_id = _method
        self.args_exp_list = _args

    def __str__(self):
        temp = self.exp_type
        if self.to_print is not None:
            self.exp_type = self.to_print

        to_return = Expression.__str__(self) + str(self.method_id)

        self.exp_type = temp

        to_return += str(len(self.args_exp_list)) + "\n"
        for exp in self.args_exp_list:
            to_return += str(exp)
        return to_return

    def cgen(self, ro, imp_map, st):
        method_offset = -1
        for i, method in enumerate(imp_map[ro]):
            if method.name_id == self.method_id.id:
                method_offset = i + vtable_methods_offset
        if method_offset == -1:
            print("Could not find method; Self_Dispatch")
            exit(1)

        for i, arg in enumerate(reversed(self.args_exp_list)):
            arg_loc = arg.cgen(ro, imp_map, st)
            pr("push %s" % arg_loc)

        # get vtable pointer
        log("get vtable pointer self")
        pr("ld %s <- %s[%d]" % (rtmp, rself, vtable_offset))

        pr("ld %s <- %s[%d]" % (rtmp, rtmp, method_offset))

        call(rtmp)

        for i, arg in enumerate(reversed(self.args_exp_list)):
            pr("pop %s" % rtmp)

        return racc

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

    def cgen(self, ro, imp_map, st):
        pred_loc = self.pred_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (rtmp, pred_loc, attributes_offset))
        pr("bnz %s True%d" % (rtmp, Utilities.count))
        pr("bz %s False%d" % (rtmp, Utilities.count))
        # true branch
        Utilities.output += "True%d:\n" % Utilities.count
        ret_loc = self.then_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (racc, ret_loc))
        pr("jmp Fi%d" % Utilities.count)
        # false branch
        Utilities.output += "False%d:\n" % Utilities.count
        ret_loc = self.else_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (racc, ret_loc))
        pr("jmp Fi%d" % Utilities.count)
        # end label
        Utilities.output += "Fi%d:\n" % Utilities.count
        Utilities.count += 1
        return racc

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

    def cgen(self, ro, imp_map, st):
        start_label = "WhileStart%d" % Utilities.count
        end_label = "WhileEnd%d" % Utilities.count
        Utilities.count += 1

        Utilities.output += start_label + ":\n"
        pred_loc = self.pred_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (rtmp, pred_loc, attributes_offset))
        pr("bz %s %s" % (rtmp, end_label))

        body_loc = self.body_exp.cgen(ro, imp_map, st)

        pr("jmp %s" % start_label)
        Utilities.output += end_label + ":\n"

        pr("li %s <- %d" % (racc, 0))


        return racc

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

    def cgen(self, ro, imp_map, st):
        for exp in self.body_exp_list:
            exp.cgen(ro, imp_map, st)
        return racc

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

    def cgen(self, ro, imp_map, st):
        pr("la %s <- %s..new" % (rtmp, self.class_id.id))
        call(rtmp)
        return racc

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

    def cgen(self, ro, imp_map, st):
        exp_loc = self.e_exp.cgen(ro, imp_map, st)
        pr("bz %s IsVoid%d" % (racc, Utilities.count))
        # not void
        pr("li %s <- %s" % (rtmp, 0))
        pr("jmp IsVoidEnd%d" % Utilities.count)
        # is void
        Utilities.output += "IsVoid%d:\n" % Utilities.count
        pr("li %s <- %s" % (rtmp, 1))
        pr("jmp IsVoidEnd%d" % Utilities.count)
        # end of is void
        Utilities.output += "IsVoidEnd%d:\n" % Utilities.count
        pr("push %s" % rtmp)
        new = New(self.lineno, Identifier(self.lineno, "Bool"))
        new_loc = new.cgen(ro, imp_map, st)
        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))
        pr("mov %s <- %s" % (racc, new_loc))
        Utilities.count += 1
        return racc

    def get_type(self, cl, M, O, ast):
        e_type = self.e_exp.get_type(cl, M, O, ast)
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
    def cgen(self, ro, imp_map, st):
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (x_loc, x_loc, attributes_offset))

        pr("push %s" % x_loc)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        pr("pop %s" % rtmp)

        pr("mov %s <- %s" % (racc, y_loc))
        pr("ld %s <- %s[%d]" % (racc, racc, attributes_offset))

        pr("add %s <- %s %s" % (racc, rtmp, racc))

        pr("push %s" % racc)

        new = New(self.lineno, Identifier(self.lineno, "Int"))
        new_loc = new.cgen(ro, imp_map, st)

        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))

        return new_loc



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

    def cgen(self, ro, imp_map, st):
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (x_loc, x_loc, attributes_offset))

        pr("push %s" % x_loc)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        pr("pop %s" % rtmp)

        pr("mov %s <- %s" % (racc, y_loc))
        pr("ld %s <- %s[%d]" % (racc, racc, attributes_offset))

        pr("sub %s <- %s %s" % (racc, rtmp, racc))

        pr("push %s" % racc)

        new = New(self.lineno, Identifier(self.lineno, "Int"))
        new_loc = new.cgen(ro, imp_map, st)

        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))

        return new_loc

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

    def cgen(self, ro, imp_map, st):
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (x_loc, x_loc, attributes_offset))

        pr("push %s" % x_loc)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        pr("pop %s" % rtmp)

        pr("mov %s <- %s" % (racc, y_loc))
        pr("ld %s <- %s[%d]" % (racc, racc, attributes_offset))

        pr("mul %s <- %s %s" % (racc, rtmp, racc))

        pr("push %s" % racc)

        new = New(self.lineno, Identifier(self.lineno, "Int"))
        new_loc = new.cgen(ro, imp_map, st)

        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))

        return new_loc

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

    def cgen(self, ro, imp_map, st):
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (x_loc, x_loc, attributes_offset))

        pr("push %s" % x_loc)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        # TODO: Divide by zero check should probably go here

        pr("pop %s" % rtmp)

        pr("mov %s <- %s" % (racc, y_loc))
        pr("ld %s <- %s[%d]" % (racc, racc, attributes_offset))

        pr("div %s <- %s %s" % (racc, rtmp, racc))

        pr("push %s" % racc)

        new = New(self.lineno, Identifier(self.lineno, "Int"))
        new_loc = new.cgen(ro, imp_map, st)

        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))

        return new_loc

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

    def cgen(self, ro, imp_map, st):
        # TODO: I don't think this handles custom object comparison
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (rtmp, x_loc))
        pr("ld %s <- %s[%d]" % (rtmp, rtmp, attributes_offset))

        pr("push %s" % rtmp)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (y_loc, y_loc, attributes_offset))

        pr("pop %s" % rtmp)
        pr("blt %s %s LT%d" % (rtmp, y_loc, Utilities.count))
        log("Greater than or equal to")
        pr("li %s <- %d" % (racc, 0))
        pr("jmp LTEnd%d" % Utilities.count)

        # Less than branch
        Utilities.output += "LT%d:\n" % Utilities.count
        pr("li %s <- %d" % (racc, 1))
        pr("jmp LTEnd%d" % Utilities.count)

        # end label
        Utilities.output += "LTEnd%d:\n" % Utilities.count
        pr("push %s" % racc)
        pr("la %s <- %s..new" % (racc, "Bool"))
        call(racc)
        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))

        Utilities.count += 1
        return racc

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

    def cgen(self, ro, imp_map, st):
        # TODO: I don't think this handles custom object comparison
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (rtmp, x_loc))
        pr("ld %s <- %s[%d]" % (rtmp, rtmp, attributes_offset))

        pr("push %s" % rtmp)
        y_loc = self.y_exp.cgen(ro, imp_map, st)

        pr("ld %s <- %s[%d]" % (y_loc, y_loc, attributes_offset))

        pr("pop %s" % rtmp)
        pr("ble %s %s LE%d" % (rtmp, y_loc, Utilities.count))
        log("Greater than")
        pr("li %s <- %d" % (racc, 0))
        pr("jmp LEEnd%d" % Utilities.count)

        # Less than branch
        Utilities.output += "LE%d:\n" % Utilities.count
        pr("li %s <- %d" % (racc, 1))
        pr("jmp LEEnd%d" % Utilities.count)

        # end label
        Utilities.output += "LEEnd%d:\n" % Utilities.count
        pr("push %s" % racc)
        pr("la %s <- %s..new" % (racc, "Bool"))
        call(racc)
        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))

        Utilities.count += 1
        return racc

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

    def cgen(self, ro, imp_map, st):
        # TODO: I don't think this handles custom object comparison
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (rtmp, x_loc))
        pr("ld %s <- %s[%d]" % (rtmp, rtmp, attributes_offset))

        pr("push %s" % rtmp)
        y_loc = self.y_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (y_loc, y_loc, attributes_offset))

        pr("pop %s" % rtmp)
        pr("beq %s %s EQ%d" % (rtmp, y_loc, Utilities.count))
        log("Not equals")
        pr("li %s <- %d" % (racc, 0))
        pr("jmp EQEnd%d" % Utilities.count)

        # Less than branch
        Utilities.output += "EQ%d:\n" % Utilities.count
        pr("li %s <- %d" % (racc, 1))
        pr("jmp EQEnd%d" % Utilities.count)

        # end label
        Utilities.output += "EQEnd%d:\n" % Utilities.count
        pr("push %s" % racc)
        pr("la %s <- %s..new" % (racc, "Bool"))
        call(racc)
        pr("pop %s" % rtmp)
        pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))

        Utilities.count += 1
        return racc

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

    def cgen(self, ro, imp_map, st):

        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (rtmp, x_loc, attributes_offset))

        pr("bz  %s Not%d" % (rtmp, Utilities.count))
        log("Not 0")
        pr("li %s <- %d" % (rtmp, 0))
        pr("jmp NotEnd%d" % Utilities.count)

        # Less than branch
        Utilities.output += "Not%d:\n" % Utilities.count
        pr("li %s <- %d" % (rtmp, 1))
        pr("jmp NotEnd%d" % Utilities.count)

        # end label
        Utilities.output += "NotEnd%d:\n" % Utilities.count
        pr("st %s[%d] <- %s" % (x_loc, attributes_offset, rtmp))

        Utilities.count += 1
        return x_loc

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

    def cgen(self, ro, imp_map, st):
        log("Negate")
        x_loc = self.x_exp.cgen(ro, imp_map, st)
        pr("ld %s <- %s[%d]" % (rtmp, x_loc, attributes_offset))
        pr("push %s" % x_loc)
        pr("li %s <- -1" % racc)
        pr("mul %s <- %s %s" % (rtmp, racc, rtmp))
        pr("pop %s" % racc)
        pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))
        return racc

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

    def cgen(self, ro, imp_map, st):
        new = New(self.lineno, Identifier(self.lineno, "Int"))
        new_loc = new.cgen(ro, imp_map, st)

        pr("li %s <- %d" % (rtmp, self.int_const))
        pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))

        return racc

    def get_type(self, cl, M, O, ast):
        self.exp_type = "Int"
        return self.exp_type


class String(Expression):
    str_const = None
    label = None

    def __init__(self, _lineno, _str, _label):
        Expression.__init__(self, _lineno)
        self.exp_name = "string"
        self.str_const = _str
        self.label = _label

    def __str__(self):
        to_return = Expression.__str__(self)
        to_return += str(self.str_const) + "\n"
        return to_return

    def cgen(self, ro, imp_map, st):
        pr("la %s <- %s" % (racc, self.label))
        return racc

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

    def cgen(self, ro, imp_map, st):
        pr("ld %s <- %s" % (racc, st[self.var_id.id]))
        return racc

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

    def cgen(self, ro, imp_map, st):
        new = New(self.lineno, Identifier(self.lineno, "Bool"))
        new_loc = new.cgen(ro, imp_map, st)
        pr("li %s <- %d" % (rtmp, 1))
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))
        return racc

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

    def cgen(self, ro, imp_map, st):
        new = New(self.lineno, Identifier(self.lineno, "Bool"))
        new_loc = new.cgen(ro, imp_map, st)
        pr("li %s <- %d" % (rtmp, 0))
        pr("st %s[%d] <- %s" % (new_loc, attributes_offset, rtmp))
        return racc

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

    def cgen(self, ro, imp_map, st):
        # let bindings
        new_section("Let bindings", 1)
        curr_length = len(st)


        for i, attr in enumerate(self.binding_list):
            total_offset = attributes_offset + i + curr_length
            pr("la %s <- %s..new" % (rtmp, attr.type_id.id))
            call(rtmp)
            if attr.value_exp is not None:
                pr(";; cgen LET expression initializer")

                res = attr.value_exp.cgen(ro, imp_map, st)

                pr("st %s[%d] <- %s" % (rself, total_offset, res))
            else:
                pr("li %s <- 0" % rtmp)
                pr("st %s[%d] <- %s" % (rself, attributes_offset + i, rtmp))
            st[attr.var_id.id] = rself.off(total_offset)

        exp_loc = self.body_exp.cgen(ro, imp_map, st)
        pr("mov %s <- %s" % (racc, exp_loc))
        return racc

    def get_type(self, cl, M, O, ast):
        additional_O = []
        for binding in self.binding_list:
            additional_O.append((binding.var_id.id, binding.type_id.id))
            type = None
            if binding.value_exp is not None:
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

    def cgen(self, ro, imp_map, st):
        log("Case expression")
        exp_loc = self.case_exp.cgen(ro, imp_map, st)
        pr("push %s" % exp_loc)
        pr("ld %s <- %s[%d]" % (racc, exp_loc, vtable_offset))
        # TODO: Runtime error for case on void here.

        ending_label = "CaseEnd%d" % Utilities.count
        Utilities.count += 1
        for elem in self.case_elem_list:
            elem.label = "Case%d" % Utilities.count
            pr("la %s <- %s..vtable" % (rtmp, elem.type_id.id))
            pr("beq %s %s %s" % (racc, rtmp, elem.label))
            Utilities.count += 1

        # TODO: Runtime error for no case here.
        for elem in self.case_elem_list:
            Utilities.output += elem.label + ":\n"
            st_copy = st.copy()
            st_copy[elem.var_id.id] = Utilities.FP(0)
            exp_loc = elem.body_exp.cgen(ro, imp_map, st_copy)
            pr("mov %s <- %s" % (racc, exp_loc))
            pr("jmp %s" % ending_label)



        Utilities.output += ending_label + ":\n"
        pr("pop %s" % rtmp)
        return racc

    def get_type(self, cl, M, O, ast):
        exp_type = self.case_exp.get_type(cl, M, O, ast)

        common_parent = None
        for elem in self.case_elem_list:
            elem_type = elem.type_id.id
            body_type = elem.body_exp.get_type(cl, M, [(elem.var_id.id, elem_type)] + O, ast)
            if common_parent is None:
                common_parent = Identifier(0, body_type)
            else:
                common_parent = self.mutual_parent(common_parent, Identifier(0, body_type), ast, cl)

            if elem_type == "SELF_TYPE":
                print("ERROR: " + elem.type_id.lineno +
                      ": Type-Check: no SELF_TYPE in case statements ")
                exit(1)
            if elem_type is not None and not self.is_parent_of(elem.type_id, Identifier(0, elem_type), ast, cl):
                print("ERROR: " + self.lineno +
                      ": Type-Check: types don't match in case ")
                exit(1)

        self.exp_type = common_parent.id

        if self.exp_type is None:
            self.exp_type = "Object"

        return self.exp_type


class Case_Elem(object):
    var_id = None
    type_id = None
    body_exp = None
    label = None

    def __init__(self, _var, _type, _body):
        self.var_id = _var
        self.type_id = _type
        self.body_exp = _body

    def __str__(self):
        return str(self.var_id) + str(self.type_id) + str(self.body_exp)

class Internal(Expression):
    method_name = None

    def __init__(self, _lineno, _method):
        Expression.__init__(self, _lineno)
        self.exp_name = "internal"
        self.method_name = _method

    def cgen(self, ro, imp_map, st):
        my_method = None
        for method in imp_map[ro]:
            if (ro + "." + method.name_id) == self.method_name:
                my_method = method
                break

        for i, formal in enumerate(reversed(my_method.formals_list)):
            pr("push %s" % st[formal.name_id])
        pr("la %s <- %s" % (rtmp, self.method_name))
        call(rtmp)
        return racc

        """


        if self.method_name == "Object.Abort":


            return racc
        if self.method_name == "IO.out_int":
            v_loc = st[my_method.formals_list[0].name_id]
            pr("ld %s <- %s" % (racc, v_loc))
            pr("mov %s <- %s" % (rtmp, racc))

            pr("ld %s <- %s[%d]" % (rtmp, rtmp, attributes_offset))
            pr("mov r1 <- %s" % rtmp)
            pr("syscall IO.out_int")

            return racc
        if self.method_name == "IO.out_string":
            v_loc = st[my_method.formals_list[0].name_id]
            pr("ld %s <- %s" % (racc, v_loc))


            pr("syscall IO.out_string")

            return racc

        if self.method_name == "Object.type_name":
            new = New(self.lineno, Identifier(self.lineno, "String"))
            new_loc = new.cgen(ro, imp_map, st)

            pr("ld %s <- %s[%d]" % (rtmp, rself, vtable_offset))
            pr("ld %s <- %s[%d]" % (rtmp, rtmp, vtable_object_offset))
            pr("st %s[%d] <- %s" % (racc, attributes_offset, rtmp))

            return racc
        else:
            pr(";; Placeholder")
            pr(";; Placeholder")
            pr(";; Placeholder")
            pr(";; Placeholder")
            pr(";; Placeholder")
            return racc
        """

