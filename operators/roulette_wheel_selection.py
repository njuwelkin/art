
''' Roulette Wheel Selection implementation. '''

from random import random
from bisect import bisect_right

from datetime import datetime

class RouletteWheelSelection(object):
    def __init__(self):
        '''
        Selection operator with fitness proportionate selection(FPS) or
        so-called roulette-wheel selection implementation.
        '''
        pass

    def accumulate(self, fits):
        ret = [fits[0]]
        for i in range(1, len(fits)):
            ret.append(fits[i] + ret[i - 1])
        return ret

    def select(self, population, fitness):
        '''
        Select a pair of parent using FPS algorithm.
        '''
        # Normalize fitness values for all individuals.
        fit = population.all_fits(fitness)
        min_fit = min(fit)
        fit = [(i - min_fit) for i in fit]

        # Create roulette wheel.
        sum_fit = sum(fit)
        wheel = self.accumulate([i/sum_fit for i in fit])
        wheel[population.size - 1] = 1.0
        
        # Select a father and a mother.
        father_idx = bisect_right(wheel, random())
        father = population[father_idx]
        mother_idx = (father_idx + 1) % len(wheel)
        mother = population[mother_idx]

        return father, mother

