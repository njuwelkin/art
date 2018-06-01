from copy import deepcopy
import numpy as np
from scipy import sparse
from random import random

from art_config import *


class Triangle(object):
    def __init__(self, vertex=None, color=None, rand = False):
        if not rand:
            self.vertex = vertex    # ((x1, y1), (x2, y2), (x3, y3))
            self.color = color      # (r, g, b)
        else:
            vertex = []
            for i in range(0, 3):
                v = (int(CanvasSize*random()), int(CanvasSize*random()))
                vertex.append(v)
            self.vertex = tuple(vertex)

            self.color = (int(256*random()), int(256*random()), int(256*random()))

class ArtIndividual(object):
    def __init__(self, rand = True):
        if rand:    # random
            self.chromsome = []
            for i in range(0, ChromLen):
                self.chromsome.append(Triangle(rand=True))

    def setChrom(self, chrom):
        assert len(chrom) == ChromLen
        self.chromsome = chrom
        return self

    def clone(self):
        indv = self.__class__(rand=False)
        indv.setChrom(deepcopy(self.chromsome))
        return indv




if __name__ == '__main__':
    a=ArtIndividual(2)
    print "***************"
    print a.chromsome
    print len(a.chromsome)
    print a.chromsome.sum()
    print "***************"
    print a.mat
    print a.mat.sum()
    print "***************"
    print a.solution
    print len(a.solution)
