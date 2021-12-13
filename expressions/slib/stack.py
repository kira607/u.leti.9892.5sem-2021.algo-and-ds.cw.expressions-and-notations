class Stack:
    def __init__(self, *args):
        self.stack = []
        for arg in args:
            self.push(arg)

    def __bool__(self):
        return len(self.stack) != 0

    def push(self, value):
        self.stack.append(value)

    def pop(self, index=None):
        return self.stack.pop(index) if index else self.stack.pop()

    def top(self):
        return self.stack[-1]