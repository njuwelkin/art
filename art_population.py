from multiprocessing import Pool
from art_individual import ArtIndividual

class Population(object):

    def __init__(self, fitness, size=100):
        if size % 2 != 0:
            raise ValueError('Population size must be an even number')
        self.size = size
        self._updated = False
        self._individuals = []
        self._calc = MultTaskCalFitness(4, fitness)

    def init(self, indvs=None):
        IndvType = ArtIndividual

        if indvs is None:
            for _ in range(self.size):
                indv = IndvType(1)
                self._individuals.append(indv)
        else:
            # Check individuals.
            if len(indvs) != self.size:
                raise ValueError('Invalid individuals number')
            for indv in indvs:
                if not isinstance(indv, IndividualBase):
                    raise ValueError('individual class must be subclass of IndividualBase')
            self.individuals = indvs

        self._updated = True

        return self

    def update_flag(self):
        '''
        Interface for updating individual update flag to True.
        '''
        self._updated = True

    @property
    def updated(self):
        return self._updated

    def new(self):
        return self.__class__(indv_template=self.indv_template,
                              size=self.size)

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
            #self._fitness = [fitness(indv) for indv in self._individuals]
            self._fitness = self._calc.calculate(self._individuals)
        return self._fitness



def cal_fitness_task(idx, part, fitness):
    return (idx, [fitness(a) for a in part])

class MultTaskCalFitness(object):
    def __init__(self, processes, fitness):
        self.processes = processes
        self.pool = Pool(processes=4)
        self.fitness = fitness

    def calculate(self, l):
        results= []
        start = 0
        total_len = len(l)
        part_len = total_len / self.processes
        for i in range(0, self.processes):
            end = start+part_len
            if end > total_len:
                end = total_len

            part = l[start:start+part_len]
            ret = self.pool.apply_async(cal_fitness_task, args=(i, part, self.fitness))
            results.append(ret)

        real_results = [r.get() for r in results]
        real_results = sorted(real_results, key=lambda a: a[0])
        
        ret = []
        for r in real_results:
            ret.extend(r[1])
        return ret





