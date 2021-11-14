from subsection import Subsection


class Layout:
    def __init__(self, subsections):
        self.subsections = [Subsection(rows) for rows in subsections]

    def block_alternate_seats(self):
        for subsection in self.subsections:
            subsection.block_alternate_seats()

    def getSubsections(self):
        return self.subsections

    def toJSON(self):
        return self.subsections
