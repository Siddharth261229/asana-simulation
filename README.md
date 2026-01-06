# Asana RL Environment: High-Quality Seed Data Generator

This repository contains a robust data generation pipeline designed to create realistic, enterprise-scale seed data for a Reinforcement Learning (RL) environment simulating Asana.

---

## Overview

Frontier AI models require high-fidelity environments to learn complex computer-use tasks. This project simulates a B2B SaaS company (**TechFlow SaaS**) with **5,000 employees** and **~80,000 tasks**, creating a database rich in relational complexity, temporal consistency, and linguistic variety.

The generated dataset serves as the **ground truth state** for an RL agent learning to navigate project management workflows, ensuring the agent encounters realistic challenges rather than simplified toy data.

---

## Key Features

- **Enterprise Scale:** Simulates an organization with 5,000 users, 250 teams, and 2,000+ active projects.
- **Hierarchical Schema:** Implements a realistic Asana data model:  
  `Org → Team → Project → Section → Task → Subtask`
- **Temporal Consistency:** Ensures tasks are not completed before creation and due dates respect business days (Mon–Fri).
- **Context-Aware Content:** Generates department-specific task names (e.g., Engineering vs. Marketing).
- **Workload Clustering:** Simulates real-world usage patterns using a Zipfian distribution (20% users handle 80% tasks).

---

## Repository Structure

```text
asana-simulation/
├── README.md
├── requirements.txt
├── schema.sql
├── .env.example
├── output/
│   └── asana_simulation.sqlite
└── src/
    ├── main.py
    ├── config.py
    ├── generators/
    │   ├── users.py
    │   ├── projects.py
    │   └── tasks.py
    └── utils/
        ├── db.py
        ├── llm_client.py
        └── helpers.py
```

````

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/asana-simulation.git
cd asana-simulation
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

Dependencies include:

- Faker
- tqdm
- python-dotenv

---

## Usage

### 1. Configure the Simulation

Edit `src/config.py`:

```python
NUM_USERS = 5000
NUM_TEAMS = 250
PROJECTS_PER_TEAM = 8
TASKS_PER_PROJECT = 40
```

These defaults generate the full enterprise-scale dataset. Reduce values for testing.

---

### 2. Run the Generator

```bash
python src/main.py
```

---

### 3. Execution Flow

1. Initializes database (`output/asana_simulation.sqlite`)
2. Generates users and roles
3. Builds team and project hierarchy
4. Populates tasks with realistic timelines

**Expected runtime:** 2–5 minutes on a standard laptop.

---

## Output

The final dataset is stored at:

```text
output/asana_simulation.sqlite
```

You can inspect it using:

- DB Browser for SQLite
- DBeaver

---

## Methodology & Design

### Data Realism Strategies

- **Task Naming:** Uses structured templates rather than generic labels.
- **Weekend Logic:** Due dates avoid Saturdays and Sundays.
- **Causal Integrity:** Ensures `completed_at > created_at`. Overdue tasks receive realistic delay offsets.

---

## 🔌 Extensibility

The `MockLLM` in `src/utils/llm_client.py` can be replaced with real LLM calls.

Steps:

1. Add your API key to `.env`
2. Replace template logic with actual OpenAI API calls.

---

## License / Attribution

Created for **Research Scientist Internship Assignment — January 2026**.

```

---


```
````
