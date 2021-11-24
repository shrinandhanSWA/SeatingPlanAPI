from seating.subsection import Subsection


class Layout:

    def __init__(self, subsections):

        output = []
        total_seats = 0
        for rows in subsections:
            subsection = Subsection(rows)
            total_seats += subsection.get_total_seats()
            output.append(subsection)

        self.subsections = output
        self.total_seats = total_seats

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

    def get_total_seats(self):
        return self.total_seats