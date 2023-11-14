from lmd.semantic_analysis.type_analyser import TypeAnalyser
from lmd.ast.visitor import Visitor


class DefinitionSearcher(Visitor):
    def __init__(self):
        self.definitions = {}

    def search(self, asts):
        for ast in asts:
            self.visit(ast)
        return self.definitions

    def visit_const_node(self, node):
        self.definitions[node.name()] = node


class Type:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Type[{self.name}]"


class TypeVariable(Type):
    def __init__(self, name):
        super().__init__(name)

    def __eq__(self, other):
        return type(other) == TypeVariable and other.name == self.name


class TypeConstructor(Type):
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def __str__(self):
        args = " " + " ".join(self.args)
        return self.name + (args if self.args else "")


class FunctionType(TypeConstructor):
    def __init__(self, arg_type, result_type):
        super().__init__('->', [arg_type, result_type])
        self.arg_type = arg_type
        self.result_type = result_type

    def __str__(self):
        if isinstance(self.arg_type, FunctionType):
            arg = f"({self.arg_type})"
        else:
            arg = f"{self.arg_type}"
        return f"{arg} -> {self.result_type}"

    def __repr__(self):
        if isinstance(self.arg_type, FunctionType):
            arg = f"({self.arg_type})"
        else:
            arg = f"{self.arg_type}"
        return f"FunctionType[{arg} -> {self.result_type}]"

    def new(arg_types, result_type):
        if len(arg_types) == 1:
            return FunctionType(arg_types[0], result_type)
        else:
            return FunctionType(arg_types[0], FunctionType.new(arg_types[1:], result_type))


class Error(Type):
    def __init__(self):
        super().__init__("Inference Error")


class Scheme:
    def __init__(self, params, type):
        self.params = params
        self.type = type

    def __str__(self):
        return " => ".join(self.params) + " => " + str(self.type)


class Substitution:
    def __init__(self, mapping=None):
        self.mapping = mapping or {}

    def apply(self, t):
        if isinstance(t, TypeVariable):
            return self.mapping.get(t.name, t)
        elif isinstance(t, FunctionType):
            return FunctionType(self.apply(t.arg_type), self.apply(t.result_type))
        elif isinstance(t, Scheme):
            return self.apply_to_scheme(t)
        else:
            return t

    def apply_to_scheme(self, scheme):
        pruned_mapping = {
            k: v
            for k, v in self.mapping.items()
            if k not in scheme.params
        }
        return Scheme(scheme.params, Substitution(pruned_mapping).apply(scheme.type))

    def after(self, other):
        return Substitution(
            {
                **self.mapping,
                **{
                    k: self.apply(v)
                    for k, v in other.mapping.items()
                }
            }
        )


class TypeVariables:
    def __init__(self):
        self.next_id = 0

    def new(self):
        result = TypeVariable(f"t{self.next_id}")
        self.next_id += 1
        return result


class Context:
    def __init__(self):
        self.stack = [({}, Substitution())]

    def push(self, ctx, subst=None):
        subst = subst or Substitution()
        old_ctx, old_subst = self.stack[-1]
        self.stack.append(({**old_ctx, **ctx}, subst.after(old_subst)))

    def apply(self, subst):
        old_ctx, old_subst = self.stack[-1]
        self.stack[-1] = (old_ctx, subst.after(old_subst))

    def pop(self):
        self.stack.pop()

    def lookup(self, name):
        ctx, subst = self.stack[-1]
        if name in ctx:
            return subst.apply(ctx[name])


class TypeAnalyser(Visitor):
    def __init__(self, report):
        self.type_variables = TypeVariables()
        self.context = Context()
        self.report = report

    def analyse(self, asts):
        definitions = DefinitionSearcher().search(asts)
        self.context.push({name: Scheme([], self.type_variables.new())
                          for name in definitions
                           })
        for name, definition in definitions.items():
            t, s = self.visit(definition)
            self.context.apply(s)
            s = self.unify(t, self.get_type_of(name))
            self.context.apply(s)

        for name in definitions:
            t = self.context.lookup(name)
            print(name, ":", self.prettify(t))

    def prettify(self, t):
        params = self.free_variables(t)
        if len(params) <= 26:
            alphabetic_params = [chr(ord('a') + i) for i in range(len(params))]
            subst = Substitution(
                {param: alphabetic for param, alphabetic in zip(params, alphabetic_params)})
            params = alphabetic_params
        else:
            subst = Substitution()

        if len(params) == 0:
            return t.type
        else:
            return Scheme(params, subst.apply(t.type))

    def get_type_of(self, name):
        result = self.context.lookup(name)
        if result is None:
            print(f"unknown identifier {name}")
        else:
            return self.instantiate(result)

    def visit_qualified_identifier_node(self, node):
        name = node.path[-1].token.text
        return self.get_type_of(name), Substitution()

    def visit_parenthesised_expression_node(self, node):
        return self.visit(node.expression)

    def visit_const_node(self, node):
        args = [node.token.text for node in node.names[1:]]

        arg_types = [self.type_variables.new() for _ in args]
        ctx = {}
        for name, t in zip(args, arg_types):
            ctx[name] = Scheme([], t)
        self.context.push(ctx)
        result_type, s = self.visit(node.value)
        arg_types = [s.apply(arg) for arg in arg_types]
        self.context.pop()
        if len(arg_types) == 0:
            return result_type, s
        else:
            return FunctionType.new(arg_types, result_type), s

    def visit_binary_expression_node(self, node):
        return TypeConstructor('Int'), Substitution()

    def visit_function_call_node(self, node):
        result_type = self.type_variables.new()

        function_type, s = self.visit(node.function)
        arg_types = []
        for arg_node in node.arguments:
            self.context.push({}, s)
            t, s2 = self.visit(arg_node)
            self.context.pop()
            arg_types.append(t)
            s = s2.after(s)

        s1 = self.unify(s.apply(function_type),
                        FunctionType.new(arg_types, result_type))
        return s1.apply(result_type), s1.after(s)

    def visit_token_node(self, node):
        return TypeConstructor('Int'), Substitution()

    def instantiate(self, scheme):
        subst = Substitution({
            param: self.type_variables.new()
            for param in scheme.params
        })

        return subst.apply(scheme.type)

    def unify(self, t1, t2):
        if isinstance(t1, TypeConstructor) and isinstance(t2, TypeConstructor):
            if t1.name == t2.name:
                s = Substitution()
                for a1, a2 in zip(t1.args, t2.args):
                    s1 = self.unify(s.apply(a1), s.apply(a2))
                    s = s1.after(s)
                return s
            else:
                print(f"Cannot unify types: `{t1}`, `{t2}`")
        elif isinstance(t1, TypeVariable):
            return self.var_bind(t1.name, t2)
        elif isinstance(t2, TypeVariable):
            return self.var_bind(t2.name, t1)
        else:
            print(f"Cannot unify types: {t1}, {t2}")
            return Substitution()

    def var_bind(self, name, t):
        if t == TypeVariable(name):
            return Substitution()
        elif name in self.free_variables(t):
            print(
                f"Cannot unify variable {name} with {t}. Occurs check failed.")
            return Substitution()
        else:
            return Substitution({name: t})

    def free_variables(self, t):
        if isinstance(t, TypeVariable):
            return [t.name]
        elif isinstance(t, TypeConstructor):
            if len(t.args) > 0:
                result = []
                for a in t.args:
                    for v in self.free_variables(a):
                        if v not in result:
                            result.append(v)
                return result
        elif isinstance(t, Scheme):
            result = []
            for v in self.free_variables(t.type):
                if v not in t.params:
                    result.append(v)
            return result
        return []


def analyse_semantics(asts, report):
    TypeAnalyser(report).analyse(asts)
