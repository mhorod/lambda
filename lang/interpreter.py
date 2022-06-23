from lang.context import ContextStack
from lang.ast import *
from lang.tokens import *


class RuntimeError(BaseException):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class Value:
    '''Wrapper for a runtime value'''

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return to_string(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Function:
    def __init__(self, name, args, expr, ctx=None, target=None, applied=None):
        self.target = target or self
        self.name = name
        self.args = args
        self.expr = expr
        self.ctx = ctx.flat() if ctx is not None else ContextStack()
        # Add self to the context to enable recursion
        if self.name is not None:
            self.ctx[self.name] = self
        self.applied = applied or []

    def __call__(self, values):
        applied = self.applied + values
        if type(self.args) == VArgs or len(values) == len(self.args):
            return self.target.evaluate_result(applied)
        elif len(values) > len(self.args):
            raise RuntimeError("Too many arguments")
        else:
            index = len(values)
            return Function(self.name, self.args[index:], self.expr, self.ctx,
                            self, applied)

    def __repr__(self):
        if type(self.args) != VArgs:
            args = ' '.join(str(i) for i in self.args)
            applied = self.target.applied_ctx(self.applied)
            where = ", ".join(f"{key}={value}"
                              for key, value in applied.items())
            where = f" where {where}" if where else ""
            return f"Fn({args} => {self.expr}{where})"
        else:
            return f"Fn(vargs => {self.expr})"

    def evaluate_result(self, values):
        call_ctx = {arg: value for arg, value in zip(self.args, values)}
        call_ctx = {**self.applied_ctx(values), **call_ctx}
        self.ctx.push(call_ctx)
        value = evaluate_expression(self.expr, self.ctx)
        self.ctx.pop()
        return value

    def applied_ctx(self, values):
        applied = {}
        for i, value in enumerate(values):
            applied[self.args[i]] = value
        return applied


class BuiltInFunction(Function):
    def __init__(self, args, f):
        super().__init__(None, args, None)
        self.f = f

    def evaluate_result(self, values):
        values = [arg.value if type(arg) == Value else arg for arg in values]
        result = self.f(*values)
        if type(result) != Function and type(result) != Value:
            return Value(result)
        else:
            return result

    def __repr__(self):
        return "BuiltInFunction"


class VArgs:
    pass


def to_string(value):
    if type(value) == list and all(
            type(c) == str and len(c) == 1 for c in value):
        return "".join(value)
    else:
        return str(value)


def add_builtins(ctx):
    ctx['print'] = BuiltInFunction(['x'], lambda x: print(to_string(x)))

    # Math
    ctx['+'] = BuiltInFunction(['a', 'b'], lambda x, y: x + y)
    ctx['-'] = BuiltInFunction(['a', 'b'], lambda x, y: x - y)
    ctx['*'] = BuiltInFunction(['a', 'b'], lambda x, y: x * y)
    ctx['/'] = BuiltInFunction(['a', 'b'], lambda x, y: x / y)
    ctx['//'] = BuiltInFunction(['a', 'b'], lambda x, y: x // y)

    # Comparisons
    ctx['=='] = BuiltInFunction(['a', 'b'], lambda a, b: a == b)
    ctx['!='] = BuiltInFunction(['a', 'b'], lambda a, b: a != b)
    ctx['<'] = BuiltInFunction(['a', 'b'], lambda x, y: x < y)
    ctx['<='] = BuiltInFunction(['a', 'b'], lambda x, y: x <= y)
    ctx['>'] = BuiltInFunction(['a', 'b'], lambda x, y: x > y)
    ctx['>='] = BuiltInFunction(['a', 'b'], lambda x, y: x >= y)

    # Logical
    ctx['true'] = True
    ctx['false'] = False
    ctx['and'] = BuiltInFunction(['a', 'b'], lambda x, y: x and y)
    ctx['or'] = BuiltInFunction(['a', 'b'], lambda x, y: x or y)
    ctx['not'] = BuiltInFunction(['x'], lambda x: not x)

    # List functions
    ctx['list'] = []
    ctx['\''] = BuiltInFunction(VArgs(), lambda *args: list(args))
    ctx['singleton'] = BuiltInFunction('x', lambda x: [x])
    ctx['head'] = BuiltInFunction(['x'], lambda x: x[0])
    ctx['tail'] = BuiltInFunction(['x'], lambda x: x[1:])
    ctx['cons'] = BuiltInFunction(['head', 'tail'], lambda x, y: [x] + y)
    ctx['len'] = BuiltInFunction(['x'], lambda x: len(x))

    # Casts
    ctx['int'] = BuiltInFunction(['x'], lambda x: int(to_string(x)))
    ctx['str'] = BuiltInFunction(['x'], lambda x: list(str(x)))

    # Create fresh new contex to allow shadowing
    ctx.push()


def run_instructions(instructions, argv, ctx=None):
    ctx = ContextStack(ctx)
    add_builtins(ctx)
    try:
        for instruction in instructions:
            if type(instruction) == Let:
                run_let(instruction, ctx)
            elif type(instruction) == OpenScope:
                ctx.push()
            elif type(instruction) == CloseScope:
                ctx.push()
        if ctx['main'] is None:
            raise RuntimeError("main function not found")
        else:
            argv = [Value(list(str(arg))) for arg in argv]
            ctx['main']([argv])
    except RuntimeError as e:
        print("ERROR:", e)


def run_let(let, ctx):
    if let.name in ctx.top():
        raise RuntimeError(f"{let.name} already declared")

    if len(let.args) == 0:
        ctx[let.name] = evaluate_expression(let.expr, ctx)
    else:
        ctx[let.name] = Function(let.name, let.args, let.expr, ctx)


def evaluate_expression(expr, ctx):
    if type(expr) == str:
        if expr in ctx:
            return ctx[expr]
        else:
            raise RuntimeError(f"Use of undeclared identifier: {expr}")
    elif type(expr) == Expression:
        return evaluate_expression(expr.value, ctx)
    elif type(expr) == Call:
        return evaluate_call(expr, ctx)
    elif type(expr) == If:
        return evaluate_if(expr, ctx)
    elif type(expr) == Fn:
        return Function(None, expr.args, expr.expr, ctx)
    elif type(expr) == Block:
        return evaluate_block(expr, ctx)
    elif type(expr) == Number:
        return Value(int(expr.text))
    elif type(expr) == String:
        return Value(list(expr.text))
    else:
        raise RuntimeError(f"Invalid expression: {expr}")


def evaluate_block(expr, ctx):
    ctx.push()
    result = None
    for instruction in expr.instructions:
        if type(instruction) == Let:
            run_let(instruction, ctx)
        else:
            result = evaluate_expression(instruction, ctx)
    ctx.pop()
    return result


def evaluate_call(expr: Call, ctx):
    fn = evaluate_expression(expr.fn, ctx)
    if fn is None:
        raise RuntimeError(f"Use of undeclared function: {expr.name}")
    arg_values = [evaluate_expression(arg, ctx) for arg in expr.args]
    return fn(arg_values)


def evaluate_if(expr, ctx):
    condition = evaluate_expression(expr.condition, ctx)
    if condition.value:
        return evaluate_expression(expr.true_expr, ctx)
    else:
        return evaluate_expression(expr.false_expr, ctx)


def get_number(value):
    try:
        return int(value)
    except:
        return None
