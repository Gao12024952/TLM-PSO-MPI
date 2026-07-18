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
- **Local evolution interval:** `GENL = 4`
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
