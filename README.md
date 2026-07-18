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

- **Python:** 3.12.4
- **Python environment:** Anaconda base environment
- **mpi4py:** 4.0.3
- **openpyxl:** 3.1.2

Install the required Python packages using:

```bash
pip install -r requirements.txt
