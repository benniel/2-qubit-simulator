import numpy as np
from .quantum_state import QState

class QGate1:
    ''' A generic 1-qubit gate '''

    def __init__(self, unitary_matrix):
        self.u = unitary_matrix

    @property
    def u(self):
        return self._u
        test_transformation = np.matmul(self.u, np.array([0,1]))
        msg = "Transformations must be unitary"
        assert np.linalg.norm(test_transformation) == 1.0, msg

    @u.setter
    def u(self, u):
        self._u = u

    def apply(self, qubit):
        qubit.state = np.matmul(self.u, qubit.state)
        return qubit

class QGate2:
    ''' A generic 2-qubit gate '''

    def __init__(self, unitary_matrix):
        self.u = unitary_matrix

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, u):
        self._u = u
        test_transformation = np.matmul(self.u, np.array([0,0,0,1]))
        msg = "Transformations must be unitary"
        assert np.linalg.norm(test_transformation) == 1.0, msg

    def apply(self, q1, q2):
        psi = q1.interact(q2)
        return QState(self.u.dot(psi.state))

