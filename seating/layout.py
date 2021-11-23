from seating.subsection import Subsection


class Layout:

    def __init__(self, subsections):

        output = []

        for rows in subsections:
            output.append(Subsection(rows))

        self.subsections = output

    def block_alternate_seats(self):
        for subsection in self.subsections:
            subsection.block_alternate_seats()

    def get_subsections(self):
        return self.subsections

    def to_json(self):
        return self.subsections

    def get_seat_mapping(self):
        seats = {}

        for subsection in self.subsections:
            seats.update(subsection.get_seat_mapping())

        return seats
