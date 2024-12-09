# xAI-chess
# Overview
This repository consists of several experiments to explore the realm of explainability for deep reinforcement learning (DRL) models. Specifically, we use chess environments to be able to effectively explain a model's underlying thought process and reasoning. We present 4 novel methods that attempt to explore different avenues of explainability:<br>
**(1)** Extend the SARFA framework to evaluate the importance of feature absences through additive perturbations. <br>
**(2)** Extend the SARFA framework to identify offensive versus defensively salient features in adversarial environments.<br>
**(3)** Use a novel technique called Sequential SARFA, which uses temporal perturbations on top of naive SARFA, to improve performance.<br>
**(4)** A novel framework called Pairwise Importance for RL Sensitivity or PaIRS for highlighting important groups of features to explain RL decision-making and potential strategies.<br>

Please look at our [paper](https://github.com/radroof22/xAI-chess/blob/main/SARFA%2BExtending%20Explainability%20in%20Chess.pdf) for more details or [video](https://www.youtube.com/watch?v=Nf51Pvb5ju8&ab_channel=RitheshRajasekar) for more details.

Additionally, we would like to give credits to the authors of the SARFA paper as many of our experiments use SARFA as a basis for further developments and improvements. Furthermore, we would like to give the authors of SARFA credit for both the chess_saliency_dataset_v1.json dataset file and core.py file which contains the default implementation of SARFA adapted from the SARFA repository. <br>
[SARFA repository](https://github.com/nikaashpuri/sarfa-saliency/tree/master)

__Authors__: Rithesh Rajasekar, Rohan Mehta, Arsh Singhal, Rishi Ramen

# Setup

In order to replicate all the experiments in this repository, you will only need access to CPU resources.
You will need to install a conda environment with all the required packages. Please run the following commands below for the full set up:
```bash
cd {parent}/xAI-chess
conda create --name chess_env python=3.9
conda activate chess_env
pip install -r requirements.txt
```

# Run Experiments

- For experiment 1, please run sarfa_empty_spaces.ipynb notebook
- For experiment 2, please run sarfa_offense_defense.ipynb notebook
- for experiment 3, please run the sarfa_baseline.ipynb notebook and sequential_sarfa.ipynb
- for experiment 4, please run the pairs_groups.ipynb notebook

# Folders
- `chess_dataset/` contains the dataset itself (`chess_saliency_dataset_v1.json`) and code for loading the dataset and running benchmarks
- `pair_results/` contains experimental qualitative results for the PaIRS algorithm
- `sarfa/` contains classes and methods for the baseline SARFA implementation. It also includes visualization functions for understanding the output
- `test_fens/` contains curated dataset of FENS (special chess notation for describing a board) used for testing experiments 1,2, and 4. The FEN you want to test can be chosen by its index in the notebooks.
