from .block import Block

class Seat(Block):
    def __init__(self, seat_no, row, column, occupant=None):
        self.seat_no = seat_no
        self.occupant = occupant
        self.available = True
        self.row = row
        self.column = column

    def set_occupant(self, occupant):
        self.occupant = occupant

    def is_available(self):
        return self.available

    def set_unavailable(self):
        self.available = False

    def __str__(self):
        if not self.available:
            return f"|XX|"
        elif not self.occupant:
            return f"|__|"

        return f'|{self.occupant}|'