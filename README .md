# 🧠 Surgical Scheduling with Reinforcement Learning

A Deep Reinforcement Learning project for optimizing patient scheduling in operating rooms.  
Developed as part of a university course in RL, this project simulates a dynamic hospital environment and trains intelligent agents to learn efficient and fair scheduling strategies.

---

## 🚀 Project Overview

This repository includes:

- A custom Gym environment for modeling operating room scheduling.
- RL agents trained with DQN, PPO, and A2C algorithms.
- Baseline policies (Random, Heuristic) for comparison.
- Visualizations, performance metrics, and simulation video.
- A fully documented notebook with reproducible experiments.

---

## 📂 Folder Structure

```
.
├── Agent.ipynb                 # Main notebook: training, tuning, evaluation, visualizations
├── env.py                      # Custom Gym environment for surgical scheduling
├── simulation_agent.mp4        # Rendered video of the trained A2C agent in action
├── Final_RL_Project_Report.pdf    # Full academic report documenting the entire project
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation

├── Rewards logger/             # Saved reward logs for each agent
│   ├── rewards_logger_a2c.pkl
│   ├── rewards_logger_dqn.pkl
│   └── rewards_logger_ppo.pkl

├── Trained Agents/             # Serialized RL agents
│   ├── trained_a2c.zip
│   ├── trained_dqn.zip
│   └── trained_ppo.zip

```

---

## ⚙️ Installation

1. Clone the repository:

```
git clone https://github.com/Razelbaz1/surgical-scheduler-rl.git
cd surgical-scheduler-rl
```

2. Create a virtual environment (recommended) and install dependencies:

```
pip install -r requirements.txt
```

---

## 📒 How to Use

Open the main notebook:

```
jupyter notebook Agent.ipynb
```

The notebook is organized as follows:

- Environment setup and exploration
- Training DQN, PPO, and A2C agents
- Hyperparameter search
- Performance comparison (with summary tables & graphs)
- Evaluation against random and greedy baselines
- Animated simulation of the trained A2C agent

---

## 🎬 Agent Simulation

Run the final cell in `Agent.ipynb` to generate the video `simulation_agent.mp4`.

You can also open the video file directly to see the trained A2C agent scheduling urgent and non-urgent patients across 3 operating rooms.

---
## 📄 Final Report
The file `Final_RL_Project_Report.pdf` provides a comprehensive summary of the project.
It includes background theory, environment and algorithm design, training methodology, comparative results, visualization outputs, and academic discussion.
This document is especially useful for readers seeking a formal overview of the project's methodology and conclusions.

---
## 📖 Academic Reference

This project was inspired by:

**u, H., Fang, Y., Chou, C.-A., Fard, N., & Luo, L. (2023). A reinforcement learning-based optimal control approach for managing an elective surgery backlog after pandemic disruption. Health Care Management Science, 26, 430–446**  
*A reinforcement learning‑based optimal control approach for managing an elective surgery backlog after pandemic disruption*  

---

## 🧑‍💻 Author

Final project by **Noa Anaki, Raz Elbaz, Osher Digurker**  
Course: Introduction to Reinforcement Learning  
Department of Industrial Engineering & Management  
Ariel University, 2025

---
