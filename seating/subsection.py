from seating.seat import Seat


class Subsection:
    def __init__(self, rows, reqs, people):
        self.rows = []
        self.seats = {}

        build = []

        for row in rows:
            this_row = []
            for count in row:
                seat = Seat(count)
                if str(count) in reqs:
                    # find person and set occupant
                    for person in people:
                        if person.get_name() == reqs[str(count)]:
                            seat.set_occupant(person)
                            seat.set_unavailable()
                            break

                this_row.append(seat)

            build.append(this_row)

        self.rows = build


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
                    person = people.pop()

                    if person:
                        seat.set_occupant(person)
                        seat.set_unavailable()

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