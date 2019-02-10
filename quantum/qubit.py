import numpy as np
from .quantum_state import QState

class Qubit:
    ''' A generic qubit '''

    def __init__(self, alpha=None, beta=None):
        if alpha is None:
            alpha = np.random.random()
        if beta is None:
            beta = np.random.random()
        state = np.array([alpha, beta])
        self.state = np.array(state)/np.linalg.norm(state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        msg = 'Not a normalised state'
        assert(1 - np.sum([x**2 for x in self.state]) < 1e-6), msg

    def interact(self, qubit):
        ''' interact with another qubit to produce a 2-qubit system '''
        q1 = self.state
        q2 = qubit.state
        interfere = np.array([q1[0] * q2[0], # amplitude of 00
                              q1[0] * q2[1], # amplitude of 01
                              q1[1] * q2[0], # amplitude of 10
                              q1[1] * q2[1]]) # amplitude of 11
        normalised = interfere/np.linalg.norm(interfere)
        return QState(normalised)
