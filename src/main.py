import os
# Import all necessary config variables
from src.config import NUM_USERS, NUM_TEAMS, PROJECTS_PER_TEAM, TASKS_PER_PROJECT
from src.utils.db import init_db
from src.utils.helpers import generate_uuid
from src.generators.users import generate_users
from src.generators.projects import generate_teams_and_projects
from src.generators.tasks import generate_tasks

def main():
    print("Starting Asana Simulation Data Generator...")
    print(f"Config: {NUM_USERS} users, {NUM_TEAMS} teams, {PROJECTS_PER_TEAM} projects/team, {TASKS_PER_PROJECT} tasks/project")
    
    # 1. Setup Database
    if not os.path.exists("output"):
        os.makedirs("output")
    init_db()
    
    # 2. Generate Organization & Users
    org_id = generate_uuid()
    users = generate_users(NUM_USERS)
    
    # 3. Generate Teams & Projects
    # FIX: Pass the config variables here
    projects = generate_teams_and_projects(org_id, NUM_TEAMS, PROJECTS_PER_TEAM)
    
    # 4. Generate Tasks & Comments
    generate_tasks(projects, users, TASKS_PER_PROJECT)
    
    print("\nSimulation complete!")
    print(f"Database generated at: output/asana_simulation.sqlite")

if __name__ == "__main__":
    main()