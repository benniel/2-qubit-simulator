# 2-qubit-simulator
This is a small simulator for two-qubit systems.

## Features
### Quantum gates
* Define arbitrary 1-qubit or 2-qubit quantum gates.
* Create superpositions and entangled states by applying a sequence of gates.

### Measurements
* Make partial measurements on 2-qubit systems in arbitrary bases.

## Example: Simulate the CHSH experiment
Run `python3 chsh.py` to execute the experiment.
### The CHSH experiment
#### Setup
Alice and Bob are playing a cooperative game. They each receive one classical
bit and one qubit as input. Then they each have to output one classical bit in
response to their inputs. If the two classical input bits are both `1`, Alice
and Bob have to output different results in order to win. Otherwise, they have
to output the same result. The two qubits are known to be in the entangled
state

![](https://latex.codecogs.com/svg.latex?%5Cdpi%7B300%7D%20%5Clarge%20%7C%5CPsi%5Crangle%20%3D%20%5Cfrac%7B1%7D%7B%5Csqrt%7B2%7D%7D%20%28%7C00%5Crangle%20&plus;%20%7C11%5Crangle%29)

such that they will always give the same bit result when measured in the computational
basis. Alice and Bob may devise a strategy in advance, but they are not allowed
to communicate during the game.


#### The classical case assumes locality
In a classical universe, the state of the two qubits are completely defined,
even if Alice and Bob can't tell what those states are. If this assumption is
true, then nothing Alice does can affect the outcome of Bob's measurement, and
_vice versa_.

The best strategy is for Alice and Bob to both always output `0`. In this way,
they can target 3 out of 4 possible configurations of their classical bits.
They can therefore expect to win the game with 0.75 probability:

| Alice | Bob | Desired Result |
|-------|-----|----------------|
| 0     | 0   | Same           |
| 0     | 1   | Same           |
| 1     | 0   | Same           |
| 1     | 1   | Different      |

#### The quantum case assumes non-locality
In a quantum universe, information about the individual qubits are distributed
through the 2-qubit system. In particular, a partial measurement of the system 
(i.e. a measurement on one of the qubits) affects the state of the entire
system (i.e. both the measured and unmeasured qubits). If this assumption is
true, Alice and Bob can devise a strategy to increase their chances of winning.
Their best strategy is to align their measurements, such that the angle between
their respective measurement bases is known:

| Alice | Bob | Alice's basis rotation | Bob's basis rotation | Angle between bases | Probability of Same Result          |
|-------|-----|------------------------|----------------------|---------------------|-------------------------------------|
| 0     | 0   | ![alt text](https://latex.codecogs.com/svg.latex?0.0)                    | ![](https://latex.codecogs.com/svg.latex?%5Cpi/8)                | ![alt text](https://latex.codecogs.com/svg.latex?%5Cpi/8)              | ![alt text](https://latex.codecogs.com/svg.latex?cos%5E2%28%5Cpi/8%29%5Capprox%200.85) |
| 0     | 1   | ![alt text](https://latex.codecogs.com/svg.latex?0.0)                    | ![alt text](https://latex.codecogs.com/svg.latex?-%5Cpi/8)               | ![alt text](https://latex.codecogs.com/svg.latex?-%5Cpi/8)               | ![alt text](https://latex.codecogs.com/svg.latex?cos%5E2%28-%5Cpi/8%29%5Capprox%200.85)  |
| 1     | 0   | ![alt text](https://latex.codecogs.com/svg.latex?%5Cpi/4)                  | ![alt text](https://latex.codecogs.com/svg.latex?%5Cpi/8)                | ![alt text](https://latex.codecogs.com/svg.latex?-%5Cpi/8)              | ![alt text](https://latex.codecogs.com/svg.latex?cos%5E2%28-%5Cpi/8%29%5Capprox%200.85) |
| 1     | 1   | ![alt text](https://latex.codecogs.com/svg.latex?%5Cpi/4)                  | ![alt text](https://latex.codecogs.com/svg.latex?-%5Cpi/8)               | ![alt text](https://latex.codecogs.com/svg.latex?-3%5Cpi/8)              | ![alt text](https://latex.codecogs.com/svg.latex?cos%5E2%28-3%5Cpi/8%29%5Capprox%200.15) |

The following figure illustrates the case where Alice and Bob both receive classical bits with state `0`. Their goal is to output the same result, which is achieved with probability 0.85, due to the rotations of their respective qubit measurement bases.
![](./Measurements.svg)
