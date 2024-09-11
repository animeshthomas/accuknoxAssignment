class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}
#creating rect obj
rect = Rectangle(5, 3)

for item in rect:
    print(item)
