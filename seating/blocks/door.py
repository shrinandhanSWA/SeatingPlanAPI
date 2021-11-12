from .block import Block

class Door(Block):
    def __init__(self, row, column):
        super().__init__(row, column)

    def __str__(self):
        return '|_.|'
