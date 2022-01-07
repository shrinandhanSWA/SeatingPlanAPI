from seating.seat import Seat
from seating.student import DummyStudent, is_dummy_student


class Subsection:
    def __init__(self, rows, reserved, people, blanks):
        self.valid = True
        self.seats = {}
        self.rows = self.initialise_rows(blanks, people, reserved, rows)

    def initialise_rows(self, blanks, people, reserved, rows):
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
                    seat.set_occupant(DummyStudent())
                    seat.set_unavailable()
                    this_available = False

                if str(count) in reserved:
                    if not this_available:
                        # trying to set student into a seat that was blanked out
                        self.valid = False
                        break
                    # find person and set occupant
                    for person in people:
                        if person.get_name() == reserved[str(count)]:
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

    def allocate_seats(self, students):
        """
        Sets random occupant for available seats
        :param students: list of students
        :return: list of students that could not be allocated
        """

        for row in self.rows:
            for seat in row:
                if seat.is_available() and seat.get_seat_no() != -1:
                    if not students:
                        return []
                    person = students.pop()

                    if person:
                        seat.set_occupant(person)
                        seat.set_unavailable()

                elif not seat.is_available() and is_dummy_student(students[-1]):
                    students.pop()

        return students

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
