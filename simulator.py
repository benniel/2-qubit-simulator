import math
import numpy as np
from tqdm import tqdm

class qgate:
    def __init__(self, unitary_matrix):
        self.u = unitary_matrix

    @property
    def u(self):
        return self._u

    @u.setter
    def u(self, u):
        self._u = u

    def apply(self, qubit):
        assert self.u.shape == (2,2)
        qubit.state = np.matmul(self.u, qubit.state)
        return qubit

    def apply2(self, q1, q2):
        psi = q1.interact(q2)
        assert self.u.shape == (4,4)
        return qustate(self.u.dot(psi.state))
                                       
class qubit:
    def __init__(self, alpha=None, beta=None):
        if alpha is None:
            alpha = np.random.random()
        if beta is None:
            beta = np.random.random()
        self.state = np.array([alpha, beta])

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        msg = 'Not a normalised state'
        assert(1 - np.sum([x**2 for x in self.state]) < 1e-6), msg

    def interact(self, qubit):
        q1 = self.state
        q2 = qubit.state
        interfere = np.array([q1[0] * q2[0], # amplitude of 00
                              q1[0] * q2[1], # amplitude of 01
                              q1[1] * q2[0], # amplitude of 10
                              q1[1] * q2[1]]) # amplitude of 11
        normalised = interfere/np.linalg.norm(interfere)
        return qustate(normalised)

class qustate:
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

def locality(n=10000):
    # This experiment assumes that the states of qubits are completely defined
    # before any measurements are made.
    win = 0
    pbar = tqdm(range(n))
    for i in range(n): # perform experiment n times
        # alice and bob each receive a random classical bit
        bob_in = np.random.choice([0,1])
        alice_in = np.random.choice([0,1])
        # and we have two correlated (but individually defined qubits)
        q1_bit = np.random.choice([0,1]) 
        q2_bit = q1_bit
        q1_sign = np.random.choice([0, 1])
        q2_sign = q1_sign

        # alice and bob can both measure either the sign or the bit value
        # of their qubits.
        # alice = np.random.choice([q1_bit, q1_sign])
        # bob = np.random.choice([q2_bit, q2_sign])
        
        # the best strategy is to ignore what they measure and just output 0
        alice = 0
        bob = 0

        if alice_in + bob_in != 2:
            if alice == bob:
                win += 1
        else:
            if alice != bob:
                win += 1
        pbar.update()
    pbar.close()
    return win/n # return win rate

def non_locality(n=10000):
    # this experiment assumes that quantum information is non-local, and that
    # a partial measurement on an entangled qubit pair modifies the state of
    # the whole system.

    # define two quantum gates: Hadamard and CNot
    hadamard = qgate(1/math.sqrt(2) * np.array([[1,1],[1,-1]]))
    cnot = qgate(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))

    win = 0
    pbar = tqdm(range(n))
    for i in range(n): # perform the experiment n times
        # alice and bob each receive a random classical bit
        bob_input_bit = np.random.choice([0,1])
        alice_input_bit = np.random.choice([0,1])

        # we have two qubits
        q1 = qubit(1,0)
        q2 = qubit(1,0)

        # entangle the two qubits by creating a Bell state
        hadamard.apply(q1)
        psi = cnot.apply2(q1, q2)

        # alice receives the first qubit and measures in a basis, depending
        # on the state of her classical bit.
        alice = psi.measure(0, 0.0 if alice_input_bit == 0 else math.pi/4)

        # bob receives the second qubit and measures in a basis, depending
        # on the state of his classical bit
        bob = psi.measure(1, math.pi/8 if bob_input_bit == 0 else -math.pi/8)

        if alice_input_bit + bob_input_bit != 2:
            if alice == bob:
                win += 1
        else:
            if alice != bob:
                win += 1
        pbar.update()
    pbar.close()
    return win/n # return win rate

if __name__=='__main__':
    quantum = non_locality(10000)
    classical = locality(100000)
    print(f'Correlated results with non-locality: {quantum*100:.3f}%')
    print(f'Correlated results with locality:     {classical*100:.3f}%')

