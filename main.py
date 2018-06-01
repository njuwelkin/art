import sys
import numpy as np
import math
from art_population import *
from operators.uniform_crossover import *
from operators.roulette_wheel_selection import *

from art_individual import *
from art_image import *
from art_mutation import *
from art_config import *

from datetime import datetime


ap = ArtPortrait("./firefox.png")
v2 = ap.v()
v2 = np.array(v2, dtype="float64")
#maxD2 = 256*256*VLen*VLen*3

def fitnessCos(indv):
    ac = ArtCanvas(indv)
    v1 = ac.v()
    v1 = np.array(v1, dtype="float64")
    a = v1 - v1.sum()/v1.size
    b = v2 - v1.sum()/v2.size
    return (sum(a*b)**2 / (sum(v1**2) * sum(v2**2)))

def fitness(indv):
    ac = ArtCanvas(indv)
    v1 = ac.v()
    v1 = np.array(v1, dtype="float64")
    d2 = sum((v1 - v2)**2)
    return 1 / (d2+1)

def display(indv):
    ac = ArtCanvas(invd)
    cv2.imshow("cv2", ac.canvas)
    cv2.waitKey(100)

class Engine(object):
    def __init__(self, population, selection, crossover, mutation, fitness, ng):
        self.population = population
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.fitness = fitness
        self.ng = ng

    def snapshot(self, best_indv, g, max):
        ac = ArtCanvas(best_indv)
        ac.save("./output/g%s_fit%s.jpg" % (g, max))

    def changePm(self, g):
        if g == self.ng / 2:
            self.mutation.setPm(0.05)
        elif g == self.ng / 4:
            self.mutation.setPm(0.1)
        elif g == 0:
            self.mutation.setPm(0.1)

    def run(self):
        #latestDrawMax = 0.5
        for g in range(self.ng):

            self.changePm(g)
            print("Generation %s start on %s" % (g, datetime.now()))
            best_indv = self.population.best_indv(self.fitness)
            max = self.population.max(self.fitness)

            if g % 5 == 0:
                self.snapshot(best_indv, g, max)
                if g % 100 == 0:
                    self.population.save("./history/population%s.npy" % g)

            maxfit = self.population.max(self.fitness)
            meanfit = self.population.mean(self.fitness)
            minfit = self.population.min(self.fitness)
            print("     max     fitness %s" % maxfit)
            print("     mean    fitness %s" % meanfit)
            print("     min     fitness %s" % minfit)
            print("     fitFactor: %s" % self.population.fitFactor)

            if (maxfit / minfit) < 2:
                self.population.fitFactor += 1
            elif (maxfit / minfit) > 4:
                fitFactor = self.population.fitFactor
                self.population.fitFactor = 1 if fitFactor == 1 else (fitFactor-1)

            indvs = []
            local_size = self.population.size // 2
            for _ in range(local_size):
                parents = self.selection.select(self.population, fitness=self.fitness)
                children = self.crossover.cross(*parents)
                children = [self.mutation.mutate(child, self) for child in children]
                indvs.extend(children)

            indvs[0] = best_indv
            self.population._individuals = indvs
            self.population.update_flag()
                

def main(argv):
    resume = len(argv) > 1

    population = Population(size=100, processes = 4)
    if not resume:
        population.init()
    else:
        print "load"
        population.load(argv[1])

    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    mutation = Mutation(pm=0.4)

    engine = Engine(population, selection, crossover, mutation, fitness, 50000)
    engine.run()

if __name__ == '__main__':
    main(sys.argv)

