from seating.seat import Seat


class Subsection:
    def __init__(self, rows):
        self.rows = []
        self.seats = {}

        count = 0
        build = []

        for row in rows:
            this_row = []
            for _ in row:
                seat = Seat(count)
                this_row.append(seat)
                count += 1

            build.append(this_row)

        self.rows = build
        self.total_seats = count

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
                if seat.is_available() and seat.get_seat_no() != -1:
                    if not people:
                        return []
                    seat.set_occupant(people.pop())

        return people

    def get_total_seats(self):
        return self.total_seats

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