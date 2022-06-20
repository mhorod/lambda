class Annotation:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Annotation(self.text)"


class Let:
    def __init__(self, name, args, expr):
        self.name = name
        self.args = args
        self.expr = expr

    def __repr__(self):
        arg_str = ''
        for arg in self.args:
            arg_str += " " + str(arg)

        return f"Let({self.name}{arg_str} = {self.expr})"


class Expression:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Expr({str(self.value)})"


class Block:
    def __init__(self, instructions):
        self.instructions = instructions

    def __repr__(self):
        return f"Block({';'.join(str(i) for i in self.instructions)}"


class Call:
    def __init__(self, fn, args):
        self.fn = fn
        self.args = args

    def __repr__(self):
        args = " ".join(str(i) for i in self.args)
        return f"Call({self.fn} {args})"


class If:
    def __init__(self, condition, true_expr, false_expr):
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __repr__(self):
        return f"If({self.condition} then {self.true_expr} else {self.false_expr})"


class Import:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Import({self.name})"


class Fn:
    def __init__(self, args, expr):
        self.args = args
        self.expr = expr

    def __repr__(self):
        args = " ".join(str(i) for i in self.args)
        return f"Fn({args} => {self.expr})"


class OpenScope:
    pass


class CloseScope:
    pass
