import unittest
from seating.factors import GENDER
from seating.fitness_scorer import FitnessScorer
from seating.seating_arrangement import SeatingArrangement
from seating.student import Student


class TestFitnessScorer(unittest.TestCase):
    def test_fitness(self):
        factors = [GENDER]
        fitness_scorer = FitnessScorer(factors)

        std1 = Student("Alice", "a123", 'female', 'UK', None)
        std2 = Student("Bob", "b123", 'female', 'UK', None)
        std3 = Student("Charlie", "b123", 'male', 'UK', None)
        seating_arrangement = SeatingArrangement([std1, std2, std3], factors)

        self.assertEqual(fitness_scorer.fitness(seating_arrangement), 1)


if __name__ == '__main__':
    unittest.main()