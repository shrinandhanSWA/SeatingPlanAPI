class Block:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def toJSON(self):
        return self.__dict__