class Stack:
    class _MISSING(object):
        pass

    def __init__(self, *args):
        self.stack = []
        for arg in args:
            self.push(arg)

    def __bool__(self):
        return len(self.stack) != 0

    def __len__(self):
        return len(self.stack)

    def empty(self):
        return not bool(self)

    def push(self, value):
        self.stack.append(value)

    def pop(self, default=_MISSING, index=None):
        try:
            return self.stack.pop(index) if index else self.stack.pop()
        except Exception as e:
            if default is not self._MISSING:
                return default
            raise e

    def top(self):
        return self.stack[-1]