import math
import numpy as np

class QState:
    ''' A generic 2-qubit state '''

    def __init__(self, state_matrix):
        self._state = state_matrix

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        msg = 'Not a normalised state'
        assert(1 - np.sum([x**2 for x in self.state]) < 1e-6), msg

    def measure(self, bit, basis_rotation=0, name=''):
        # make a partial measurement on a 2-qubit system in an arbitrary basis.
        # amplitudes are represented in the order [00, 01, 10 ,11]
        assert bit in [0, 1]
        psi = {} 
        if bit == 0: # measure bit 0
            # get amplitudes in computational basis
            amplitude0 = self.state[0] + self.state[1]
            amplitude1 = self.state[2] + self.state[3]
            # apply arbitrary basis rotation (radians)
            theta = math.acos(amplitude0) + basis_rotation
            # calculate amplitudes in new basis
            amplitude0 = math.cos(theta)
            amplitude1 = math.sin(theta)
            # the new state will depend on the observation later
            psi[0] = np.array([math.cos(math.acos(self.state[0])+basis_rotation),
                               math.cos(math.acos(self.state[1])+basis_rotation), 0, 0])
            psi[1] = np.array([0, 0, math.sin(math.asin(self.state[2])+basis_rotation),
                               math.sin(math.asin(self.state[3])+basis_rotation)])
        elif bit == 1: # measure bit 1
            # get amplitudes in computational basis
            amplitude0 = self.state[0] + self.state[2]
            amplitude1 = self.state[1] + self.state[3]
            # apply arbitrary basis rotation (radians)
            theta = math.acos(amplitude0) + basis_rotation
            # calculate amplitudes in new basis
            amplitude0 = math.cos(theta)
            amplitude1 = math.sin(theta)
            # the new state will depend on the observation later
            psi[0] = np.array([math.cos(math.acos(self.state[0])+basis_rotation),
                               0, 0, math.cos(math.acos(self.state[2])+basis_rotation)])
            psi[1] = np.array([0, math.sin(math.asin(self.state[1])+basis_rotation), 0,
                               math.sin(math.asin(self.state[3])+basis_rotation)])
        p0 = amplitude0**2
        p1 = amplitude1**2
        #make probabalistic choice
        res = np.random.choice([0,1], p=(p0, p1))
        #collapse state
        self.state = psi[res] / np.linalg.norm(psi[res])
        return res
