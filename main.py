import numpy as np
import math
from components.population import *
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
            t = VLen_f/2 - math.sqrt((i - center[0])**2 + (j - center[1])**2)
            w[i, j] = t if t > 0 else 0
    return w.reshape(VLen*VLen)

def drawCanvas(solution):
    ac = ArtCanvas()
    for i in range(0, len(solution)):
        for target in solution[i]:
            ac.line(i, target)
    return ac

ap = ArtPortrait("./portrait.png")
v2 = ap.v()
w = gen_weight()
maxD2 = sum(w * (v2**2))

def fitness(indv):
    ac = drawCanvas(indv.solution)
    v1 = ac.v()
    d2 = sum(w * ((v1 - v2) ** 2))
    return (maxD2 / (d2 + 1))


class Engine(object):
    def __init__(self, population, selection, crossover, mutation, fitness):
        self.population = population
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.fitness = fitness

    def run(self, ng=1000):
        for g in range(ng):
            print("Generation %s start on %s" % (g, datetime.now()))
            best_indv = self.population.best_indv(self.fitness)
            print("	max fitness %s" % self.population.max(self.fitness))
            print("	")

            indvs = []
            local_size = self.population.size // 2
            for _ in range(local_size):
                print("	%s" % _)
                parents = self.selection.select(self.population, fitness=self.fitness)
                children = self.crossover.cross(*parents)
                children = [self.mutation.mutate(child, self) for child in children]
                indvs.extend(children)
                indvs[0] = best_indv
                self.population.individuals = indvs
                self.population.update_flag()
                


if __name__ == '__main__':
    art = ArtIndividual()
    population = Population(indv_template=art, size=1000)
    population.init()

    selection = RouletteWheelSelection()
    crossover = UniformCrossover(pc=0.8, pe=0.5)
    mutation = Mutation(pm=0.1)

    engine = Engine(population, selection, crossover, mutation, fitness)
    engine.run()

    ########## test code ###########
    if False:
	    #selection.select(population, fitness)
	    art2 = ArtIndividual()

	    for i in range(0, 10):
		art3, art4 = crossover.cross(art, art2)
		print("(%s, %s)" % (sum(art3.chromsome - art.chromsome), sum(art4.chromsome - art2.chromsome)))

	    for i in range(0, 20):
		art3 = art.clone()
		mutation.mutate(art)
		if sum(art.chromsome - art3.chromsome) !=0:
		    print(sum(art.chromsome - art3.chromsome))






