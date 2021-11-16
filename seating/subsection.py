from seat import Seat

class Subsection:
    def __init__(self, rows):
        self.rows = [[Seat(seat['seatNo']) for seat in row ] for row in rows]

    def to_json(self):
        return self.seats

    def allocate_seats(self, people):
        """
        Sets random occupant for available seats
        :param people: list of people
        :return: list of people that could not be allocated
        """

        for row in self.rows:
            for seat in row:
                if seat.is_available():
                    seat.set_occupant(people.pop())

        return people

    def block_alternate_seats(self):
        """
        Blocks alternate seats for social distancing
        :return: none
        """
        for row in self.rows:
            i = 0
            while i < len(row):
                row[i].set_unavailable()
                i += 2
    
    def get_seat_mapping(self):
        seats = {}

        for row in self.rows:
            for seat in row:
                seats[seat.get_seat_no()] = seat.get_occupant().get_username()
        
        return seats
