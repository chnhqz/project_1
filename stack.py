class Stack(object):
    def __init__(self):
        self.stack = []
    def isEmpty(self):
        return self.stack == []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        if self.isEmpty():
            return IndexError, 'pop from empty stack'
        return self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def size(self):
        return len(self.stack)
    def clear(self):
        if self.isEmpty():
            return IndexError, 'clear from empty stack'
        return self.stack.clear()

# stack = Stack()
# stack.push((1, 2, 3))
# stack.push((4, 5, 6))
# print(stack.peek()[1])
# stack.clear()
# print(stack.size())

