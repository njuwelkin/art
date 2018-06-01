from random import random, uniform
from art_config import *
from art_individual import *
import numpy as np

class Mutation(object):
    def __init__(self, pm):
        #if pm <= 0.0 or pm > 1.0:
        #    raise ValueError('Invalid mutation probability')

        #self.pm = pm
        self.setPm(pm)

    def setPm(self, pm):
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

                individual.chromsome[i] = Triangle(rand=True)

            # Update solution.
            individual.setChrom(individual.chromsome)

        return individual

    def _random_gen(self):
        tmp = np.random.random(GenLen)
        return (tmp < Dencity)
        
