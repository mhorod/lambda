class ContextStack:
    """
    Context stack storing key-value pairs on each level.
    All changes on the recently pushed dict.
    Lookup prioritizes shadowed keys
    """
    def __init__(self, ctx=None):
        self.stack = [ctx or {}]

    def push(self, value=None):
        self.stack.append(value or {})

    def __setitem__(self, key, value):
        self.stack[-1][key] = value

    def pop(self):
        self.stack.pop()

    def __getitem__(self, key):
        for ctx in self.stack[::-1]:
            if key in ctx:
                return ctx[key]

    def __contains__(self, key):
        return self[key] is not None

    def __repr__(self):
        return str(self.stack)

    def flat(self):
        result = {}
        for ctx in self.stack:
            for key, val in ctx.items():
                result[key] = val
        return ContextStack(result)

    def top(self):
        return self.stack[-1]
