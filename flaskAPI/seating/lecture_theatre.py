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

    def initialise_grid(self):
        default_seat_no = 0
        for row in self.plan.split('\n'):
            row_blocks = []
            for block in row.strip().split(' '):
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

                    seat = Seat(seat_no)
                    row_blocks.append(seat)
                    self.available_seats.append(seat)

            self.grid.append(row_blocks)
        
    def allocate_random_seats(self, people):
        random.shuffle(people)

        for seat, person in zip(self.available_seats, people):
            seat.set_occupant(person)


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

    lt1.allocate_random_seats(people)
    print(lt1)