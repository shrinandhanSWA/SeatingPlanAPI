import random


class SeatingMutator:
    def __init__(self, swap_rate=0, decay_rate=1, min_swap_rate=0):
        self.swap_rate = swap_rate
        self.decay_rate = decay_rate
        self.min_swap_rate = min_swap_rate

    def mutate(self, seating_arrangement):
        swaps = int(self.swap_rate * seating_arrangement.size())
        n = seating_arrangement.size()
        i = j = 0
        for _ in range(swaps):
            first = True
            # Only swap if neither are wildcards or both are wildcards
            while first or not seating_arrangement.valid_swap(i, j):
                i = random.randint(0, n - 1)
                j = random.randint(0, n - 1)
                first = False

            seating_arrangement.swap(i, j)

        return seating_arrangement

    def update(self):
        self.swap_rate = max(self.decay_rate * self.swap_rate,
                             self.min_swap_rate)
