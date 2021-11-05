from blocks.aisle import Aisle
from blocks.door import Door
from blocks.seat import Seat
import random 

class LectureTheatre:
    def __init__(self, plan):
        self.plan = ' '.join(filter(lambda s: s, plan.strip().split(' ')))
        self.grid = []
        self.seats = {}
        self.available_seats = []
        self.initialise_grid()

    def no_of_columns(self):
        return len(self.grid[0])

    def no_of_rows(self):
        return len(self.grid)

    def initialise_grid(self):
        default_seat_no = 0
        for i, row in enumerate(self.plan.split('\n')):
            row_blocks = []
            for j, block in enumerate(row.strip().split(' ')):
                if block == 'A':
                    row_blocks.append(Aisle())

                elif block == 'D':
                    row_blocks.append(Door())

                elif block[0] == 'S':
                    seat_no_str = block[1:]

                    if seat_no_str:
                        seat_no = int(seat_no_str)
                    else:
                        seat_no = default_seat_no
                        default_seat_no += 1

                    seat = Seat(seat_no, i, j)
                    row_blocks.append(seat)
                    self.available_seats.append(seat)
                    self.seats[seat_no] = seat

            self.grid.append(row_blocks)
        
    def get_available_seats(self):
        return filter(lambda seat: seat.is_available(), self.seats.values())

    def allocate_random_seats(self, people):
        random.shuffle(people)

        for seat, person in zip(self.get_available_seats(), people):
            seat.set_occupant(person)


    def seats_are_neighbours(self, seat1, seat2):
        r1, c1 = seat1.row, seat1.column
        r2, c2 = seat2.row, seat2.column
        return abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1

    def block_neighbours(self, seat):
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

    def block_alternate_seats(self):
        for seat_no in range(len(self.seats)):
            seat = self.seats[seat_no]
            if not seat.is_available():
                continue

            self.block_neighbours(seat)
            
            if seat_no > 1:
                left_seat = self.seats[seat_no - 1]
                if self.seats_are_neighbours(left_seat, seat):
                    left_seat.set_unavailable()

            if seat_no < len(self.seats) - 1:
                right_seat = self.seats[seat_no + 1]
                if self.seats_are_neighbours(seat, right_seat):
                    right_seat.set_unavailable()





    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(map(str, row)), self.grid))


if __name__ == "__main__":
    from people.student import Student
    plan1 = '''
        D  A   S S S S S S S S S S S  A  D
        S S A   S S S S S S S S S S  A S S
        S S S A  S S S S S S S S S  A S S S
        S S S S A  S S S S S S S S A S S S S
        S S S S  A  S S S S S S S A S S S S
        S S S S   A  S S S S S S A S S S S
    '''
    lt1 = LectureTheatre(plan1)
    people = []

    for i in range(10):
        people.append(Student("Rohan", "Pandit", "rp619"))

    lt1.block_alternate_seats()
    lt1.allocate_random_seats(people)
    print(lt1)