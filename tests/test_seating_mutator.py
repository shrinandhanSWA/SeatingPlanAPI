import unittest

from seating.seating_mutator import SeatingMutator


class TestSeatingMutator(unittest.TestCase):
    def test_update(self):
        swap_rate = 0.5
        decay_rate = 0.95
        seating_mutator = SeatingMutator(swap_rate=swap_rate,
                                         decay_rate=decay_rate)
        self.assertEqual(seating_mutator.swap_rate, swap_rate)
        seating_mutator.update()
        self.assertEqual(seating_mutator.swap_rate, swap_rate * decay_rate)

    def test_min_swap_rate(self):
        swap_rate = 0.5
        decay_rate = 0.95
        min_swap_rate = swap_rate * decay_rate
        seating_mutator = SeatingMutator(swap_rate=swap_rate,
                                         decay_rate=decay_rate,
                                         min_swap_rate=min_swap_rate)
        self.assertEqual(seating_mutator.swap_rate, swap_rate)
        seating_mutator.update()
        self.assertEqual(seating_mutator.swap_rate, swap_rate * decay_rate)
        seating_mutator.update()
        self.assertEqual(seating_mutator.swap_rate, swap_rate * decay_rate)


if __name__ == '__main__':
    unittest.main()