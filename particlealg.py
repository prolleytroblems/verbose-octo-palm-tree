from particle import Particle
import numpy as np
from copy import copy
import random


class ParticleOptimizer:

    def __init__(self, n_dims, n_particles, fitness, mass=1, value_ranges=None, **kwargs):

        self.particles=[]
        pos = np.random.random((n_particles, n_dims))
        spd = 2*np.random.random((n_particles, n_dims))-1
        if value_ranges:
            value_ranges=np.asarray(value_ranges)
            pos = pos*(value_ranges[:,1]-value_ranges[:,0])+value_ranges[:,0]
        for i in range(n_particles):
            self.particles.append(Particle(pos[i], spd[i], fitness, mass=mass,
                                value_ranges=value_ranges, **kwargs))
        self.gbest=None
        self._uptodate=False
        self.fitness=fitness


    def get(self):
        return random.choice(self.gbest)

    def _get_best(self):
        best=[self.particles[0].get()]
        for i in range(1, len(self.particles)):
            position=self.particles[i].get()
            fitness=self.fitness(position)
            best_fit=self.fitness(best[0])
            if fitness>best_fit:
                best=[position]
            elif fitness==best_fit:
                best.append(position)
        return best

    def gbestprop():
        doc = "The gbest property."
        def fget(self):
            if self._uptodate:
                return self._gbest
            else:
                current_best=self._get_best()
                if not(self._gbest) or self.fitness(current_best[0])>self.fitness(self._gbest[0]):
                    self._gbest=current_best
                self._uptodate=True
                return self._gbest
        def fset(self, value):
            if value==None:
                self._gbest=None
            else:
                raise Exception("Dont mess with gbest manually")
        def fdel(self):
            del self._gbest
        return locals()
    gbest = property(**gbestprop())

    def step(self):
        for particle in self.particles:
            particle.step(random.choice(self.gbest))
        self._uptodate=False

    def get_fitness(self):
        return self.fitness(self.gbest[0])


class PermutationOptimizer(ParticleOptimizer):

    def __init__(self, n_particles, valuearray, mass=1, decoding="ordered", **kwargs):
        """Valuearray should be n_dims by n_dims, with the value at (x,y) representing
            the value of element y if in position x."""
        assert valuearray.shape[0]==valuearray.shape[1]
        if decoding=="ordered":
            self.decode=self.ordereddecode
        elif decoding=="sort":
            self.decode=self.sortdecode
        else:
            raise Exception()
        self.valuearray=valuearray
        self.cleared_array=self.prelocate(valuearray)
        self.fitness=self.make_fitness()
        self.particles=[]
        n_dims=valuearray.shape[0]
        pos = np.random.random((n_particles, n_dims))
        spd = (np.random.random((n_particles, n_dims))-0.5)
        for i in range(n_particles):
            self.particles.append(Particle(pos[i], spd[i], self.fitness,
                                    value_ranges=np.asarray([(0,0.9999)]*n_dims), mass=mass, **kwargs))
        self.gbest=None
        self._uptodate=False


    def prelocate(self, valuearray):
        self.instant_matches(valuearray)
        cleared_array=valuearray[self.exclusion_mask]
        cleared_array=valuearray[:, self.exclusion_mask]
        return cleared_array

    def instant_matches(self, valuearray):
        rowmax = np.argmax(valuearray, axis=1)
        columnmax = np.argmax(valuearray, axis=0)
        matches=[]
        for dim in range(valuearray.shape[0]):
            if columnmax[rowmax[dim]]==dim:
                matches.append(dim)
        self.exclusion_mask=np.ones((n_dims), dtype="boolean")
        self.exclution_mask[matches]=False

    def reinclude(array, excluded):
        reconstructed=[]
        arrayi=0
        excludedi=0
        for i in range(n_dims):
            if i in self.

    def get_best(self):
        return self.decode(self.gbest[0])

    def get_positions(self):
        return

    def get_all(self):
        positions=[]
        for particle in self.particles:
            positions.append(self.decode(particle.get()))
        return positions

    def ordereddecode(self, positions, **kwargs):
        slots = list(range(len(self.valuearray)))
        permutation = []
        for i in range(len(self.valuearray)):
            index = int(positions[i]*(len(self.valuearray)-i))
            permutation.append(slots.pop(index))
        return permutation

    def sortdecode(self, positions, **kwargs):
        values=list(zip(positions, range(len(self.valuearray))))
        values.sort(key=lambda x: x[0])
        permutation=list(map(lambda x: x[1], values))
        return permutation

    def evaluate(self, permutation):
        value=0
        for i in range(len(permutation)):
            value+=self.valuearray[i, permutation[i]]
        return value

    def make_fitness(self):
        def fitnessfunc(positions):
            permutation=self.decode(positions)
            return self.evaluate(permutation)
        return fitnessfunc
