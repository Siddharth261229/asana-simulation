import os

# Configuration constants
DB_PATH = os.path.join("output", "asana_simulation.sqlite")
SCHEMA_PATH = "schema.sql"

# Simulation settings for 5000 Users (Enterprise Scale)
NUM_USERS = 5000         # Target: 5,000 employees
NUM_TEAMS = 250          # Result: ~20 users per team (Realistic "Two-Pizza" rule)
PROJECTS_PER_TEAM = 8    # Result: 2,000 total active projects
TASKS_PER_PROJECT = 40   # Result: ~80,000 total tasks (over 6 months)
SIMULATION_DAYS = 180    # History length