from seating.seat import Seat


class Subsection:

    rows = []

    def __init__(self, rows):

        count = 0

        for row in rows:
            this_row = []
            for _ in row:
                seat = Seat(count)
                this_row.append(seat)
                count += 1

            self.rows.append(this_row)

    def to_json(self):
        return self.seats

    def get_rows(self):
        return self.rows

    def allocate_seats(self, people):
        """
        Sets random occupant for available seats
        :param people: list of people
        :return: list of people that could not be allocated
        """

        for row in self.rows:
            for seat in row:
                if seat.is_available():
                    if not people:
                        return []
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
