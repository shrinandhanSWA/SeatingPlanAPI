import unittest
from seating.seating_arrangement import SeatingArrangement
from seating.student import Student
from seating.factors import WILD


class TestSeatingArrangement(unittest.TestCase):
    def test_swap(self):
        """

        :return:
        """
        std1 = Student("Alice", "a123", 'female', 'UK', None)
        std2 = Student("Bob", "b123", 'male', 'UK', None)
        factors = []
        seating_arrangement = SeatingArrangement([std1, std2], factors)

        self.assertEqual(seating_arrangement.get(0), std1)
        self.assertEqual(seating_arrangement.get(1), std2)

        seating_arrangement.swap(0, 1)

        self.assertEqual(seating_arrangement.get(0), std2)
        self.assertEqual(seating_arrangement.get(1), std1)

    def test_swap_wild(self):
        """

        :return:
        """
        std1 = Student("Alice", "a123", 'female', 'UK', None, wild=True)
        std2 = Student("Bob", "b123", 'female', 'UK', None)
        factors = [WILD]
        seating_arrangement = SeatingArrangement([std1, std2], factors)

        self.assertEqual(seating_arrangement.get(0), std1)
        self.assertEqual(seating_arrangement.get(1), std2)

        seating_arrangement.swap(0, 1)

        self.assertEqual(seating_arrangement.get(0), std1)
        self.assertEqual(seating_arrangement.get(1), std2)


if __name__ == '__main__':
    unittest.main()