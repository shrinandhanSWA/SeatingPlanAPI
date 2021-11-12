from blocks.seat import Seat

def seats_are_neighbours(seat1, seat2):
    r1, c1 = seat1.row, seat1.column
    r2, c2 = seat2.row, seat2.column
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

class Subsection:
    def __init__(self, id, seats, rotation):
        self.id = id
        self.seats = []
        self.rows = len(seats)
        self.columns = len(seats[0])
        self.rotation = rotation
        self.initialise_layout(seats)

    def toJSON(self):
        dict_ = self.__dict__
        dict_['seats'] = list(map(lambda row: list(map(lambda seat: seat.toJSON(), row)), self.seats))
        return dict_

    def initialise_layout(self, seats):
        for i, row in enumerate(seats):
            curr_row = []
            for j, seat in enumerate(row):
                curr_row.append(Seat(seat['seatNo'], i, j))
                
            self.seats.append(curr_row)

    def available_seats(self):
        """
        Filters all seats that have not been allocated yet
        :return: list of seats
        """
        return list(filter(lambda seat: seat.is_available(), [seat for row in self.seats for seat in row]))

    def capacity(self):
        return len(self.available_seats())

    def allocate_seats(self, people):
        """
        Sets random occupant for available seats
        :param people: list of people
        :return: list of people that could not be allocated
        """
        capacity = self.capacity()
        remaining = people[capacity:]
        people = people[:capacity]

        for seat, person in zip(self.available_seats(), people):
            seat.set_occupant(person)

        return remaining


    def block_neighbours(self, seat):
        """
        Block seats in front, behind, left and right of current seat
        """
        row, column = seat.row, seat.column

        for dx in -1, 0, 1:
            for dy in -1, 0, 1:
                if abs(dx) + abs(dy) != 1:
                    continue

                x = row + dx
                y = column + dy

                if x < 0 or x >= self.no_of_rows() or y < 0 or y >= self.no_of_columns():
                    continue

                neighbour = self.seats[x][y]
                if isinstance(neighbour, Seat):
                    neighbour.set_unavailable()

    def block_alternate_seats(self):
        """
        Blocks alternate seats for social distancing
        :return: none
        """
        for row in self.seats:
            for seat in row:
                if not seat.is_available():
                    continue
                # block seats around the available seat
                self.block_neighbours(seat)