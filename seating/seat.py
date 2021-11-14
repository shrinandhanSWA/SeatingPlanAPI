class Seat:
    def __init__(self, seat_no):
        self.seat_no = seat_no
        self.available = True
        self.occupant = None

    def is_available(self):
        return self.available

    def set_unavailable(self):
        self.available = False
        
    def set_occupant(self, person):
        self.occupant = person