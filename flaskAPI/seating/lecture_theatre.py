from blocks.aisle import Aisle
from blocks.door import Door
from blocks.seat import Seat
import random
import json

def seats_are_neighbours(seat1, seat2):
    r1, c1 = seat1.row, seat1.column
    r2, c2 = seat2.row, seat2.column
    return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1


class LectureTheatre:
    def __init__(self, plan):
        # remove
        self.plan = plan.replace(" ", "")
        print(self.plan)
        # two-dimensional list consisting of blocks objects
        self.grid = []
        # dictionary from seat number to Seat object
        self.seats = {}
        # list of available seats
        self.available_seats = []

        self.initialise_grid()
        print(self.toJSON())

    def toJSON(self):
        return list(map(lambda row: list(map(lambda b: b.toJSON(), row)), self.grid))

    def no_of_columns(self):
        return len(self.grid[0])

    def no_of_rows(self):
        return len(self.grid)

    def initialise_grid(self):
        """
        Populates grid with block components based on lecture theatre plan
        """
        default_seat_no = 0
        for i, row in enumerate(self.plan.split('\n')):
            row_blocks = []
            for j, block in enumerate(row.split(',')):
                if block == '.':
                    row_blocks.append(Aisle(i, j))

                elif block == 'D':
                    row_blocks.append(Door(i, j))

                elif block == 'S' or block.isnumeric():
                    if block.isnumeric():
                        seat_no = int(block)
                    else:
                        # calculate seat number
                        seat_no = default_seat_no
                        default_seat_no += 1

                    seat = Seat(seat_no, i, j)
                    row_blocks.append(seat)
                    self.available_seats.append(seat)
                    self.seats[seat_no] = seat

            self.grid.append(row_blocks)

    def get_available_seats(self):
        """
        Filters all seats that have not been allocated yet
        :return: list of seats
        """
        return filter(lambda seat: seat.is_available(), self.seats.values())

    def allocate_random_seats(self, people):
        """
        Sets random occupant for available seats
        :param people: list of people
        :return: none
        """
        random.shuffle(people)

        for seat, person in zip(self.get_available_seats(), people):
            seat.set_occupant(person)

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

                neighbour = self.grid[x][y]
                if isinstance(neighbour, Seat):
                    neighbour.set_unavailable()

    def total_seats(self):
        return len(self.seats)

    def block_alternate_seats(self):
        """
        Blocks alternate seats for social distancing
        :return: none
        """
        for seat_no in range(1, len(self.seats)):
            seat = self.seats[seat_no]
            if not seat.is_available():
                continue
            # block seats around the available seat
            self.block_neighbours(seat)

            # blocks the seat before and after current one
            # if seats are in a diagonal
            if seat_no > 1:
                left_seat = self.seats[seat_no - 1]
                if seats_are_neighbours(left_seat, seat):
                    left_seat.set_unavailable()

            if seat_no < self.total_seats() - 1:
                right_seat = self.seats[seat_no + 1]
                if seats_are_neighbours(seat, right_seat):
                    right_seat.set_unavailable()

    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(map(str, row)), self.grid))


if __name__ == "__main__":
    from people.student import Student

    plan1 = '''\ 
        .,.,.,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,.,.,.,.,.,.
        .,.,.,.,.,.,.,.,.,.,.,41,40,39,38,37,36,35,34,.,.,.,.,.,.,.,.,.,.,.,.
        .,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.,.
        .,.,.,.,.,.,.,.,.,.,90,.,.,.,.,.,.,.,.,.,27,.,.,.,.,.,.,.,.,.,.
        .,.,.,.,.,.,.,.,.,89,.,.,33,32,31,30,29,28,.,.,.,26,.,.,.,.,.,.,.,.,.
        .,.,.,.,.,.,.,.,88,.,.,.,.,.,.,.,.,.,.,.,.,.,25,.,.,.,.,.,.,.,.
        .,.,.,.,.,.,.,87,.,.,79,.,.,.,.,.,.,.,.,.,.,.,.,24,.,.,.,.,.,.,.
        .,.,.,.,.,.,86,.,.,78,,.,71,.,.,.,8,.,.,.,16,.,.,.,23,.,.,.,.,.,.
        .,.,.,.,.,85,.,.,77,,.,70,,.,.,.,,7,.,.,.,15,.,.,.,22,.,.,.,.,.
        .,.,.,.,84,.,.,76,,.,69,,,.,.,.,,,6,.,.,.,14,.,.,.,21,.,.,.,.
        .,.,.,83,.,.,75,,.,68,,.,.,.,.,.,.,.,,5,.,.,.,13,.,.,.,20,.,.,.
        .,.,82,.,.,74,,.,67,,.,.,.,.,.,.,.,.,.,,4,.,.,.,12,.,.,.,19,.,.
        .,81,.,.,73,,.,66,,.,.,.,.,.,.,.,.,.,.,.,.,3,.,.,.,11,.,.,.,18,.
        80,.,.,72,,.,65,,.,.,.,.,.,.,.,.,.,.,.,.,.,.,2,.,.,.,10,.,.,.,17
        .,.,.,,.,64,,.,.,.,.,,,.,.,.,,,.,.,.,.,.,1,.,.,.,9,.,.,.\
    '''
    lt1 = LectureTheatre(plan1)
    people = []

    for i in range(10):
        people.append(Student("Rohan", "Pandit", "rp619"))

    lt1.block_alternate_seats()
    lt1.allocate_random_seats(people)
    print(lt1)
