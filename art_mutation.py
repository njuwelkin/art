from random import random, uniform
from art_config import *


class Mutation(object):
    def __init__(self, pm):
        '''
        Mutation operator with Flip Bit mutation implementation.

        :param pm: The probability of mutation (usually between 0.001 ~ 0.1)
        :type pm: float in (0.0, 1.0]
        '''
        if pm <= 0.0 or pm > 1.0:
            raise ValueError('Invalid mutation probability')

        self.pm = pm

    def mutate(self, individual, engine=None):
        '''
        Mutate the individual.
        '''
        do_mutation = True if random() <= self.pm else False

        if do_mutation:
            for i, genome in enumerate(individual.chromsome):
                no_mutate = True if random() > self.pm else False
                if no_mutate:
                    continue

                individual.chromsome[i] = int(random()*Nodes)

            # Update solution.
            individual.solution = individual.decode()

        return individual


