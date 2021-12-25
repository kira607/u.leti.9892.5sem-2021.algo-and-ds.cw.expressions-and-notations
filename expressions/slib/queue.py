from typing import Any


class Queue:
    def __init__(self, *args):
        self.queue = []
        for arg in args:
            self.put(arg)

    def put(self, value: Any) -> None:
        self.queue.insert(0, value)

    def get(self) -> Any:
        return self.queue.pop()

    def front(self):
        return self.queue[-1]