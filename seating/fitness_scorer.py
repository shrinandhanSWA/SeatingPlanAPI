from seating.factors import GENDER, NATIONALITY


class FitnessScorer:
    def __init__(self, factors):
        self.factors = factors

    def fitness(self, seating_arrangement):
        """
        Calculate the fitness of ordering of list
        :return: int
        """
        score = 0
        size = seating_arrangement.size()
        for i in range(1, size - 1):
            # Scan over every window of 3 students
            left, curr, right = seating_arrangement.get(i - 1), \
                                seating_arrangement.get(i), \
                                seating_arrangement.get(i + 1)
            if GENDER in self.factors:
                g1 = left.get_gender()
                g2 = curr.get_gender()
                g3 = right.get_gender()
                score += self.window_score(g1, g2, g3)

            if NATIONALITY in self.factors:
                n1 = left.get_nationality()
                n2 = curr.get_nationality()
                n3 = right.get_nationality()
                score += self.window_score(n1, n2, n3)

        return score

    def window_score(self, v1, v2, v3):
        score = 0
        if v1 == v2:
            score += 1

        if v2 == v3:
            score += 1

        # if all have the same gender
        if v1 == v2 == v3:
            score -= 2

        return score