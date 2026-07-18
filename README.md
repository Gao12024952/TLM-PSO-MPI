# Two-Layer Co-Evolutionary Multi-Population PSO for Multiple Path Coverage in MPI Program Mutation Testing

This repository provides the implementation and replication materials for the paper:

**“Two-Layer Co-Evolutionary Multi-Population PSO for Multiple Path Coverage in MPI Program Mutation Testing.”**

Mutation testing is widely used to evaluate the fault-detection capability of test data by introducing predefined mutations into a program under test. However, generating test data for mutation-based path coverage in MPI programs is challenging because MPI programs contain multiple concurrently executing processes, complex inter-process communications, high-dimensional input spaces, and dependencies among different process subpaths. Conventional evolutionary algorithms generally optimize each target path independently and do not fully exploit the multi-process structure of MPI programs or the relationships among multiple target paths.

To address these challenges, this work proposes a **Two-Layer Co-Evolutionary Multi-Population Particle Swarm Optimization algorithm (TLM_PSO)** for generating test data that cover multiple mutation-based paths in MPI programs.

The proposed method contains two cooperative evolution levels:

- **Inner-level cooperative evolution:** A complete multi-process mutation-based path is decomposed into multiple process subpaths. Each subprocess swarm searches only the input variables relevant to its corresponding process subpath, while the cooperative swarm coordinates the partial solutions to generate complete test inputs. This mechanism reduces redundant searches in the global input space while maintaining consistency among different process subpaths.

- **Outer-level cooperative evolution:** Target mutation-based paths are organized into aggregated and divergent path pairs according to their similarities and differences. Different information-transfer strategies are applied to the two types of path pairs. High-quality search experience is shared between aggregated paths to accelerate convergence, while heterogeneous particle information is transferred between divergent paths to improve population diversity and reduce the risk of premature convergence.

The objective of TLM_PSO is to improve the effectiveness and efficiency of automated mutation test data generation. Each particle represents a candidate test input, and the fitness function evaluates the similarity between the path traversed by that input and the target mutation-based path. The method focuses on mutation-based path coverage for deterministic or controlled MPI executions.

This repository contains the implementation of the proposed method, the MPI programs under test, baseline and ablation experiment scripts, parameter configurations, raw experimental results, and detailed instructions for reproducing the experiments reported in the paper.
