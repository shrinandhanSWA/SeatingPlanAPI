import random


class EvolutionStrategy:
    def __init__(self, mu=1, lambda_=None, epochs=1, factors=[], mutator=None,
                 scorer=None):
        self.mu = mu
        self.lambda_ = lambda_
        if self.lambda_ is None:
            self.lambda_ = self.mu * 5
        self.epochs = epochs
        self.factors = factors
        self.mutator = mutator
        self.scorer = scorer

    def run(self, orderings):
        orderings = self.initialise_population(orderings)

        for i in range(self.epochs):
            # Sort based on fitness
            orderings.sort(key=lambda students: self.scorer.fitness(students, ))
            # Select mu fittest parents
            parents = orderings[-self.mu:]

            children = []
            for _ in range(self.lambda_):
                index = random.randint(0, len(parents) - 1)
                # Mutate random parent to create new child
                children.append(self.mutator.mutate(parents[index].copy()))

            # New population is combination of parents and children
            orderings = parents + children
            self.mutator.update()

        return max(orderings, key=lambda people: self.scorer.fitness(people))

    def initialise_population(self, orderings):
        children = []
        for _ in range(len(orderings) - (self.mu + self.lambda_)):
            index = random.randint(0, len(orderings) - 1)
            # Mutate random parent to create new child
            children.append(self.mutator.mutate(orderings[index].copy()))

        orderings += children

        return orderings
