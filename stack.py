class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def get_top_element(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return False

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return False

    def print(self):
        sx = ""
        for x in self.items:
            sx += str(x) + '\t'
        print('Stack: [ {0} '.format(sx))
        return True

    def print_top3(self):
        sx = ""
        for x in self.items[-3:]:
            sx += str(x) + '\t'
        if len(self.items)>3:
            print('Stack: [ ..., {0} '.format(sx))
        else:
            print('Stack: [ {0} '.format(sx))
        return True
