from subsection import Subsection

class Layout:
    def __init__(self, rows):
        self.rows = []

        for row in rows:
            curr_row = []
            for subsec in row:
                curr_row.append(Subsection(subsec['id'], subsec['subsections'], subsec['rotation']))

            self.rows.append(curr_row)

    def getRows(self):
        return self.rows
        
