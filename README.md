# Two-Layer Co-Evolutionary Multi-Population PSO for Multiple Path Coverage in MPI Program Mutation Testing

This repository provides the implementation and replication materials for the paper **“Two-Layer Co-Evolutionary Multi-Population PSO for Multiple Path Coverage in MPI Program Mutation Testing.”**

The project implements a mutation test data generation method for multiple mutation-based path coverage in MPI programs. It combines inner-level cooperative optimization among particle swarms associated with different process subpaths with outer-level cooperative evolution among particle swarms associated with different target paths. The proposed **Two-Layer Co-Evolutionary Multi-Population Particle Swarm Optimization algorithm (TLM_PSO)** reduces redundant searches in the multi-process input space and reuses useful search information among aggregated and divergent path pairs to improve test data generation efficiency.
## 1. Environment

### 1.1 Hardware

The experiments reported in the paper were conducted using the following hardware environment:

- **Operating system:** Windows 10, 64-bit
- **CPU:** Intel Core i7 processor
- **Memory:** 16 GB RAM

### 1.2 Software

- **Python:** 3.12.4 or later
- **Python environment:** Anaconda base environment
- **mpi4py:** 4.0.3 or later
- **openpyxl:** 3.1.2 or later

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

## 2. Core Experimental Settings

The following settings are used in the implemented experiments.

### 2.1 Input Space and Process Decomposition

Each candidate test input is represented as a five-dimensional vector:

`X = (x, y, z, w, m)`

For Program P1, the input ranges are:

- **x:** `[10, 100]`
- **y:** `[40, 100]`
- **z:** `[30, 300]`
- **w:** `[20, 100]`
- **m:** `[1, 10]`

The process-relevant variable subsets are:

- **Main process:** `(x, y, z, w, m)`
- **Subprocess 1:** `(x, y, z)`
- **Subprocess 2:** `(y, z, w)`
- **Subprocess 3:** `(z, w, m)`

### 2.2 Subprocess Swarm Parameters

- **Number of subprocess swarms:** 3
- **Particle dimension:** 3
- **Swarm size:** 5
- **Inertia weight:** `w = 0.729`
- **Acceleration coefficients:** `c1 = 2.0`, `c2 = 2.0`
- **Velocity range:** `[-100, 100]`
- **Local evolution interval:** `GENL = 3`
- **Information-exchange frequency:** every 3 updates
- **Particle-migration ratio:** 30%

### 2.3 Cooperative Swarm Parameters

- **Particle dimension:** 5
- **Swarm size:** 26
- **Inertia weight:** `w = 0.729`
- **Acceleration coefficients:** `c1 = 2.0`, `c2 = 2.0`
- **Velocity range:** `[-100, 100]`
- **Global evolution interval:** `GENO = 5`
- **Information-exchange frequency:** every 5 updates
- **Particle-migration ratio:** 30%
- **Number of feedback particles:** `H = 2`

### 2.4 Outer-Level Information Exchange

- **Aggregated path pairs:** exchange high-fitness particles.
- **Divergent path pairs:** migrate low-fitness particles.
- **Received particles:** re-evaluated using the receiving target path.

## 3. Framework Overview

The following figures illustrate the construction of the program under test, the overall workflow of the proposed method, and the two-layer co-evolutionary mechanism.

### 3.1 Construction of the Program Under Test

<p align="center">
  <img src="Picture/figure1.jpg" width="95%">
</p>

<p align="center">
  <em>Figure 1. Original MPI program and the corresponding program under test after inserting mutant branches.</em>
</p>

### 3.2 Overall Framework of TLM_PSO

<p align="center">
  <img src="Picture/figure2.jpg" width="95%">
</p>

<p align="center">
  <em>Figure 2. Overall framework of the proposed Two-Layer Co-Evolutionary Multi-Population Particle Swarm Optimization algorithm (TLM_PSO).</em>
</p>

### 3.3 Two-Layer Co-Evolutionary Mechanism

<p align="center">
  <img src="Picture/figure3.jpg" width="95%">
</p>

<p align="center">
  <em>Figure 3. Two-Level Multi-Population PSO (TLM-PSO) for Co-Evolution.</em>
</p>

## 4. Core Modules


- **Path-pair determination:** Target paths are paired according to path similarity, forming aggregated path pairs with high similarity and divergent path pairs with low similarity.

- **Process-relevant variable decomposition:** The complete input vector is decomposed into variable subsets according to the variables affecting each process subpath.

- **Inner-level cooperative optimization:** Subprocess swarms search the process-relevant variable subsets, while the cooperative swarm combines and evaluates the partial solutions in the complete input space.

- **Outer-level co-evolution:**
  - **Aggregated path pairs:** High-fitness particles are exchanged to reuse useful search information and accelerate convergence.
  - **Divergent path pairs:** Low-fitness particles are migrated to introduce heterogeneous information and improve population diversity.

- **Multi-path test data generation:** The inner- and outer-level strategies are coordinated to generate test data covering multiple target mutation-based paths.
  
## 5. Algorithms

### Algorithm 1: Two-Level Co-Evolutionary Multi-Population PSO for Test Data Generation

```text
Require:
    Full target-path set P = {p_1, p_2, ..., p_L}
    PSO parameters and termination conditions

Ensure:
    Test data set covering all target mutation-based paths

1:  Initialize the particle swarm O_k for each target path p_k
2:  Initialize the subprocess swarms O_k^i using the
    process-relevant variable subsets

3:  while the termination condition is not met do
4:      for each target-path task T_k do
5:          for each subprocess swarm O_k^i do
6:              Evaluate each particle on process subpath p_k^i
7:              Update particle velocity, position, pbest, and gbest
8:          end for

9:          if the inner-level evolution condition is met then
10:             Call Algorithm 2 to perform inner-level
                cooperative optimization
11:         end if

12:         Evaluate candidate inputs on the complete path p_k
13:         Update the global best solution for T_k
14:     end for

15:     if the outer-level evolution condition is met then
16:         Call Algorithm 3 to exchange information among
            aggregated and divergent path pairs
17:     end if
18: end while

19: return the test data set covering all target paths
```

### Algorithm 2: Inner-Level Cooperative PSO for a Single Multi-Process Path

```text
Require:
    A complete target path
    p_k = p_k^0 || p_k^1 || ... || p_k^(m-1)
    PSO parameters

Ensure:
    Test data covering the complete path p_k

1:  Initialize the cooperative swarm O_k^0
2:  Initialize subprocess swarms O_k^1, ..., O_k^(m-1)

3:  while p_k is not covered and the maximum iteration
    budget is not reached do

4:      Evolve each subprocess swarm within its
        process-relevant variable subset

5:      if subprocess evolution reaches the local
        evolution interval then
6:          Select high-fitness particles from each subprocess swarm
7:          Transfer the selected particles to O_k^0
8:          Combine the partial particles to construct complete inputs
9:      end if

10:     Evolve the cooperative swarm O_k^0 in the complete
        input space

11:     if a candidate input covers p_k then
12:         Terminate the cooperative swarm and all subprocess swarms
13:     end if

14:     if cooperative-swarm evolution reaches the global
        evolution interval then
15:         Select high-fitness particles from O_k^0
16:         Decompose them according to the process-relevant variables
17:         Transfer the partial particles to the corresponding
            subprocess swarms
18:         Replace selected particles in each subprocess swarm
19:     end if
20: end while

21: return the test data covering p_k
```

### Algorithm 3: Outer-Level Co-Evolutionary PSO for Aggregated and Divergent Path Pairs

```text
Require:
    Full target-path set P = {p_1, p_2, ..., p_L}
    Aggregated path pairs
    Divergent path pairs
    PSO parameters

Ensure:
    Updated particle swarms and test data covering all target paths

1:  Establish cooperative relationships for all aggregated
    and divergent path pairs

2:  while not all target paths are covered and the maximum
    iteration budget is not reached do

3:      for each aggregated path pair <p_a, p_b> do
4:          if the information-exchange interval is reached then
5:              Select high-fitness particles from the swarm of p_b
6:              Transfer them to the corresponding swarm of p_a
7:              Re-evaluate the received particles using p_a
8:              Update the elite-particle set
9:          end if

10:         Calculate the information-transfer decision parameter
11:         if cooperative information is selected then
12:             Update particle velocities using the elite particles
13:         else
14:             Update particle velocities using standard PSO
15:         end if
16:         Update particle positions
17:     end for

18:     for each divergent path pair <p_a, p_c> do
19:         if the particle-migration interval is reached then
20:             Select low-fitness particles from the swarm of p_a
21:             Transfer them to the swarm of p_c
22:             Re-evaluate the transferred particles using p_c
23:             Replace low-fitness local particles when the
                transferred particles obtain better fitness
24:         end if
25:     end for
26: end while

27: return the test data set covering all target paths
```
