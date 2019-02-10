import math
import numpy as np
from tqdm import tqdm
from quantum.qubit import Qubit
from quantum.quantum_gate import QGate1, QGate2

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
    hadamard = QGate1(1/math.sqrt(2) * np.array([[1,1],[1,-1]]))
    cnot = QGate2(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))

    win = 0
    pbar = tqdm(range(n))
    for i in range(n): # perform the experiment n times
        # alice and bob each receive a random classical bit
        bob_input_bit = np.random.choice([0,1])
        alice_input_bit = np.random.choice([0,1])

        # we have two qubits, initialised to |0>
        q1 = Qubit(1,0)
        q2 = Qubit(1,0)

        # entangle the two qubits by creating a Bell state
        hadamard.apply(q1)
        psi = cnot.apply(q1, q2)

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
    classical = locality(100000)
    quantum = non_locality(10000)
    print(f'Classical success rate (with locality):   {classical*100:.3f}%')
    print(f'Quantum success rate (with non-locality): {quantum*100:.3f}%')

