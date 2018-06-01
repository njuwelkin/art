from multiprocessing import Pool
from art_individual import *
from art_config import *
import numpy as np

class Population(object):

    def __init__(self, size, processes = 1):
        if size % 2 != 0:
            raise ValueError('Population size must be an even number')
        self.size = size
        self._updated = False
        self._individuals = []
        self._calc = MultTaskCalFitness(processes, cal_fitness_task) if processes > 1 else None
        self.fitFactor = 1

    def init(self, indvs=None):
        IndvType = ArtIndividual

        if indvs is None:
            for _ in range(self.size):
                indv = IndvType()
                self._individuals.append(indv)
        else:
            # Check individuals.
            if len(indvs) != self.size:
                raise ValueError('Invalid individuals number')
            for indv in indvs:
                if not isinstance(indv, IndvType):
                    raise ValueError('individual class must be subclass of IndividualBase')
            self.individuals = indvs

        self._updated = True

        return self

    def save(self, path):
        all_chrom = np.zeros((self.size, ChromLen, 2, 3, 2), dtype="uint64")
        for i, indv in enumerate(self._individuals):
            for j, t in enumerate(indv.chromsome):
                all_chrom[i,j,0] = t.vertex
                all_chrom[i,j,1] = zip(t.color, (0, 0, 0))
        np.save(path, all_chrom)

    def load(self, path):
        all_chrom = np.load(path)
        for i in range(0, self.size):
            indv = ArtIndividual(rand=False)
            chroms = []
            for j in range(0, ChromLen):
                v = all_chrom[i, j, 0]
                vertex = (tuple(v[0]), tuple(v[1]), tuple(v[2]))
                c = all_chrom[i, j, 1]
                color = (int(c[0, 0]), int(c[1, 0]), int(c[2, 0]))
                t = Triangle(vertex, color)
                chroms.append(t)
            indv.setChrom(chroms)
            self._individuals.append(indv)
        self._updated = True

    def update_flag(self):
        self._updated = True

    @property
    def updated(self):
        return self._updated

    def __getitem__(self, key):
        if key < 0 or key >= self.size:
            raise IndexError('Individual index({}) out of range'.format(key))
        return self._individuals[key]

    def __len__(self):
        return len(self.individuals)

    def best_indv(self, fitness):
        all_fits = self.all_fits(fitness)
        return max(self._individuals,
                   key=lambda indv: all_fits[self._individuals.index(indv)])

    def worst_indv(self, fitness):
        all_fits = self.all_fits(fitness)
        return min(self.individuals,
                   key=lambda indv: all_fits[self.individuals.index(indv)])

    def max(self, fitness):
        return max(self.all_fits(fitness))

    def min(self, fitness):
        return min(self.all_fits(fitness))

    def mean(self, fitness):
        all_fits = self.all_fits(fitness)
        return sum(all_fits)/len(all_fits)

    def all_fits(self, fitness):
        if self._updated:
            self._updated = False
            if self._calc is None:
                self._fitness = [fitness(indv)**self.fitFactor for indv in self._individuals]
            else:
                self._fitness = self._calc.calculate(self._individuals, fitness, self.fitFactor)
        return self._fitness

def cal_fitness_task(idx, part, fitness, factor):
    return (idx, [fitness(a)**factor for a in part])

class MultTaskCalFitness(object):
    def __init__(self, processes, callback):
        self.processes = processes
        self.pool = Pool(processes=4)
        self.callback = callback

    def calculate(self, l, fitness, factor):
        results= []
        start = 0
        total_len = len(l)
        part_len = total_len / self.processes
        for i in range(0, self.processes):
            end = start+part_len
            if end > total_len:
                end = total_len

            part = l[start:start+part_len]
            ret = self.pool.apply_async(self.callback, args=(i, part, fitness, factor))
            results.append(ret)

        real_results = [r.get() for r in results]
        real_results = sorted(real_results, key=lambda a: a[0])
        
        ret = []
        for r in real_results:
            ret.extend(r[1])
        return ret



if __name__ == '__main__':
    p = Population(None, 10)
    p.init()
    p.save("history/test.npy")
    p2 = Population(None, 10)
    p2.load("history/test.npy")
    print p2._individuals[0]
    print p2._individuals[0].chromsome[0]
    print p2._individuals[0].chromsome[0].vertex
    print p._individuals[0].chromsome[0].vertex
