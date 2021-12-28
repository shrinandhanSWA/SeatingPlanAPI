from seating.seat import Seat
from seating.student import dummy_student


class Subsection:
    def __init__(self, rows, reqs, people, blanks):
        self.valid = True
        self.seats = {}
        self.rows = self.initialise_rows(blanks, people, reqs, rows)

    def initialise_rows(self, blanks, people, reqs, rows):
        build = []
        for row in rows:
            if not self.valid:
                break
            this_row = []
            for count in row:
                this_available = True
                seat = Seat(count)

                if str(count) in blanks:
                    # it is unavailable
                    # set it to the dummy person we have
                    seat.set_occupant(dummy_student())
                    seat.set_unavailable()
                    this_available = False

                if str(count) in reqs:
                    if not this_available:
                        # trying to set student into a seat that was blanked out
                        self.valid = False
                        break
                    # find person and set occupant
                    for person in people:
                        if person.get_name() == reqs[str(count)]:
                            seat.set_occupant(person)
                            seat.set_unavailable()
                            break

                this_row.append(seat)

            build.append(this_row)
        return build

    def to_json(self):
        return self.seats

    def get_rows(self):
        return self.rows

    def is_valid(self):
        return self.valid

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
