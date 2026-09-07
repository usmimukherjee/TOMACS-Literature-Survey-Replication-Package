# Literature Survey Replication Package

This repository contains the replication package for the literature survey conducted as part of the research project. It includes data, scripts, and notebooks used to generate tables and graphs for the survey.

## Abstract
Agent-Based Simulation (ABS) is a modelling framework that represents complex, real-life systems (e.g., urban transportation systems, drone swarms) as a collection of autonomous agents. In this framework, the agents make independent decisions and interact with one another within a simulated environment to mimic the real systems. Traditional ABS employs rule-based agents or equilibrium-oriented behavioural models, which often fail to adapt to shocks (i.e., unexpected scenarios), incorporate heterogeneity in decision-making, and learn strategic interactions between agents. On the other hand,  the ABS empowered by Reinforcement Learning (RL) enables its agents to learn policies through rich interactions with the environment, and can comprehensively represent search, bargaining, coordination, and competition from real-life systems (e.g., housing markets). This course will discuss current literature at the intersection of ABS and Reinforcement Learning (RL) across multiple application domains, including housing markets, transportation, energy, urban systems, and negotiation, and identify their strengths, weaknesses, and open challenges. In particular, the feasibility of applying RL agents, robustness, convergence, and policy optimization of various ABS systems will be discussed.  The Student will gain an in-depth understanding of agent-based modelling empowered by RL,  learn to integrate RL into ABS, and achieve hands-on experience with the popular ABS frameworks (e.g., Mesa).

## Repository Structure

- `data/`
  - Contains the dataset(s) used in the analysis.
  - `complete.csv`: The complete dataset used for the survey.

- `src/`
  - Contains the source code and notebooks for the analysis.
  - `Literature_Survey_Tables_and_Graphs.ipynb`: Jupyter notebook for generating tables and graphs.
  - `rq1/`, `rq2/`, `rq3/`: Subdirectories for scripts and analyses related to specific research questions.

## Supplementary Materials

This repository also includes supplementary materials that provide additional context and resources for the literature survey. These materials may include:

- Extended data descriptions
- Additional graphs and tables
- Supporting documentation for the analysis

Refer to the `supplementary/` directory for more details.

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the repository directory:
   ```bash
   cd Literature-Survey-Replication-Package
   ```

3. Open the Jupyter notebook in the `src/` directory to explore the analysis:
   ```bash
   jupyter notebook src/Literature_Survey_Tables_and_Graphs.ipynb
   ```

## License

This project is licensed under the terms of the LICENSE file included in this repository.

## Research Questions

- **RQ1**: What modelling approaches have been applied in Agent-Based Market Simulation (ABMS) systems?
- **RQ2**: What evaluation and validation methods, metrics, and subject systems are commonly used in Agent-Based Market Simulation Systems?
- **RQ3**: What are the major challenges faced in Agent-Based Market Simulation that affect the models?