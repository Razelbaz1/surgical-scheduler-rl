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
├── env.py                     # Custom environment definition
├── Agent.ipynb               # Main notebook: training, tuning, evaluation, visualizations
├── trained_a2c.zip           # Saved best-performing agent
├── simulation_agent.mp4      # Video: A2C agent simulation
├── frames/                   # PNG frames used to generate the video
├── results/                  # Reward logs and evaluation outputs
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## ⚙️ Installation

1. Clone the repository:

```
git clone https://github.com/your-username/surgical-scheduling-rl.git
cd surgical-scheduling-rl
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

## 📖 Academic Reference

This project was inspired by:

**Xu, H., Fang, Y., Chou, C.A., Fard, N., & Luo, L. (2023)**  
*A reinforcement learning‑based optimal control approach for managing an elective surgery backlog after pandemic disruption*  
Springer Nature. DOI: [link to article if public]

---

## 🧑‍💻 Author

Final project by **[Your Name]**  
Introduction to Reinforcement Learning  
Department of Industrial Engineering & Management  
Ariel University, 2025

---

## 📨 Contact

📧 your.email@example.com  
📍 Feel free to open issues or suggestions!