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

def gen_weight():
    w = np.zeros((VLen, VLen), dtype="float64")
    VLen_f = float(VLen)
    center = (VLen_f/2-0.5, VLen_f/2-0.5)
    for i in range(0, VLen):
        for j in range(0, VLen):
            #t = math.sqrt(math.fabs(VLen_f/2 - math.sqrt((i - center[0])**2 + (j - center[1])**2)))
            d = VLen_f/2 - math.sqrt((i - center[0])**2 + (j - center[1])**2)
            t = d if d > 0 else 0
            t = math.sqrt(math.sqrt(t))
            w[i, j] = t
    return w.reshape(VLen*VLen)

def drawCanvas(solution):
    ac = ArtCanvas()
    for s in solution:
        ac.line(s[0], s[1])
    return ac

ap = ArtPortrait("./portrait.png")
v2 = ap.v()
print "v2", v2.reshape(VLen, VLen)
w = gen_weight()
v2w = v2 * w
d2 = sum(v2w**2)

def fitness(indv):
    ac = drawCanvas(indv.solution)
    v1 = ac.v()
    v1w = v1 * w
    tag = 1 if (v1*v2).sum() > 0 else 0.1
    cos = (sum(v1w*v2w) ** 2) / (sum(v1w**2) * d2)  # cos(v1, v2) ^2
    return tag * cos


def display(indv):
    ac = drawCanvas(indv.solution)
    cv2.imshow("cv2", ac._canvas)
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
        ac = drawCanvas(best_indv.solution)
        ac.save("./output/g%s_fit%s.jpg" % (g, max))

    def changePm(self, g):
        if g == self.ng / 10:
            self.mutation.setPm(0.1)
        elif g == self.ng / 100:
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

            if g % 100 == 0:
                self.snapshot(best_indv, g, max)
                self.population.save("./output/population.npy")

            print("	max fitness %s" % self.population.max(self.fitness))
            print("	min fitness %s" % self.population.min(self.fitness))
            print("	total edges of best_indv: %s" % best_indv._chromsome.sum())


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

    population = Population(fitness=fitness, size=1000, processes = 4)
    if not resume:
        population.init()
    else:
        print "load"
        population.load("./output/population.npy")

    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    mutation = Mutation(pm=0.4)

    engine = Engine(population, selection, crossover, mutation, fitness, 50000)
    engine.run()

if __name__ == '__main__':
    main(sys.argv)

