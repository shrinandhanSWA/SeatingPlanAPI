from layout import Layout
from blocks.aisle import Aisle
from blocks.door import Door
from blocks.seat import Seat
import random

class LectureTheatre:
    def __init__(self, rows):
        # remove
        self.layout = Layout(rows) 
    
    def getLayout(self):
        return self.layout
    
    def toJSON(self):
        return list(map(lambda row: list(map(lambda section: section.toJSON(), row)), self.layout))

    def __str__(self):
        return '\n'.join(map(lambda row: ''.join(map(str, row)), self.layout))


if __name__ == "__main__":
    from people.student import Student

    layout = [
        [
            [
                [13, 14, 15],
                [16, 17, 18],
            ],
            [
                [7, 8, 9],
                [10, 11, 12],
            ]
        ],
        [
            [
                [1, 2, 3],
                [4, 5, 6],
            ],
            [
                [7, 8, 9],
                [10, 11, 12],
            ]
        ]
    ] 
    lt1 = LectureTheatre(layout)
    people = []

    for i in range(10):
        people.append(Student("Rohan", "Pandit", f"rp61{i}"))

    lt1.allocate_random_seats(people)
    print(lt1.toJSON())
