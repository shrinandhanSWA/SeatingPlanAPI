from seating.factors import WILD
from seating.student import is_dummy_student


class SeatingArrangement:
    def __init__(self, students, factors):
        self.students = students
        self.factors = factors

    def size(self):
        return len(self.students)

    def valid_swap(self, i, j):
        first = self.students[i]
        second = self.students[j]

        if WILD in self.factors and first.is_wildcard() != second.is_wildcard():
            return False

        if is_dummy_student(first) or is_dummy_student(second):
            return False

        return True

    def swap(self, i, j):
        self.students[i], self.students[j] = self.students[j], self.students[i]

    def copy(self):
        return SeatingArrangement(self.students.copy(), self.factors)

    def get(self, i):
        return self.students[i]

    def get_students(self):
        return self.students.copy()