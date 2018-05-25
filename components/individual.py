from copy import deepcopy


class IndividualBase(object):
    ''' Base class for individuals.
    '''
    

    def __init__(self):
        self.solution, self.chromsome = [], []

    def init(self, chromsome=None, solution=None):
        '''
        Initialize the individual by providing chromsome or solution.

        If both chromsome and solution are provided, only the chromsome would
        be used. If neither is provided, individual would be initialized randomly.

        :param chromsome: chromesome sequence for the individual
        :type chromsome: list of float/int.

        :param solution: the variable vector of the target function.
        :type solution: list of float.
        '''
        if chromsome is not None:
            self.chromsome = chromsome
            self.solution = self.decode()
        elif solution is not None:
            self.solution = solution
            self.chromsome = self.encode()
        else:
            self.solution = self._rand_solution()
            self.chromsome = self.encode()

        return self

    def clone(self):
        '''
        Clone a new individual from current one.
        '''
        indv = self.__class__()
        indv.init(chromsome=self.chromsome.copy())
        return indv


    def encode(self):
        ''' *NEED IMPLIMENTATION*
        Convert solution to chromsome sequence.

        :return chromsome: The chromsome sequence, float list.
        '''
        raise NotImplementedError

    def decode(self):
        ''' *NEED IMPLIMENTATION*
        Convert chromsome sequence to solution.

        :return solution: The solution vector, float list.
        '''
        raise NotImplementedError

    def _rand_solution(self):
        ''' Initialize individual solution randomly.
        '''
        raise NotImplementedError

