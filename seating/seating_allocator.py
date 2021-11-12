import random

class SeatingAllocator:
    def __init__(self, lecture_theatre, people, factors=['random']):
        self.layout = lecture_theatre.getLayout()
        self.people = people
        self.factors = factors

    def allocate_seats(self):
        """
        Sets random occupant for available seats
        :param people: list of people
        :return: none
        """
        if 'random' in self.factors:
            random.shuffle(self.people)

        done = False
        remaining = self.people
        rows = self.layout.getRows()
        for row in rows[::-1]:
            for subsection in row:
                remaining = subsection.allocate_seats(remaining)
                
                if not remaining:
                    done = True
                    break

            if done:
                break