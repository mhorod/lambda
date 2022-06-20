from context import ContextStack


class Type:
    def __init__(self, type_id):
        self.id = type_id


class TypeConstructor:
    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __repr__(self):
        return f"{self.name} ' '.join(str(t) for t in self.types)"


class Function(TypeConstructor):
    def __init__(self, from_type, to_type):
        super().__init__('->', [from_type, to_type])


def check_program(nodes):
    ctx = ContextStack()
    for node in nodes:
        infer_let(ctx, node)


def infer_let(ctx, node):
    name = ctx.args[0]
    args = ctx.args[1:]


def type_of_expr(ctx, node):
    pass
