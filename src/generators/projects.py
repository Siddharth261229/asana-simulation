import random
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from datetime import datetime, timedelta

# Templates for generating synthetic team names
DEPARTMENTS = ["Engineering", "Product", "Marketing", "Sales", "Operations", "HR", "Legal", "Finance"]
TEAM_SUFFIXES = ["Core", "Platform", "Growth", "Mobile", "Web", "Data", "Security", "Infra", "Support"]

PROJECT_TEMPLATES = {
    "Engineering": ["Tech Debt", "Refactor", "API Migration", "Unit Tests", "Security Audit", "V2 Launch"],
    "Product": ["Roadmap Planning", "User Research", "Beta Testing", "Feature Specs"],
    "Marketing": ["Q3 Campaign", "Social Media", "Brand Refresh", "Conference Prep", "Email Drip"],
    "Sales": ["Lead Gen", "Q4 Targets", "CRM Cleanup", "Outreach"],
    "Operations": ["Office Move", "Vendor Review", "Budget Planning", "Onboarding"]
}

SECTIONS = ["Backlog", "To Do", "In Progress", "Code Review", "Done"]

def generate_teams_and_projects(org_id, num_teams, num_projects_per_team):
    print(f"Generating {num_teams} teams and ~{num_teams * num_projects_per_team} projects...")
    conn = get_connection()
    cur = conn.cursor()
    
    generated_projects = []
    
    # Create Organization
    cur.execute("INSERT OR IGNORE INTO organizations (id, name, domain) VALUES (?, ?, ?)", 
                (org_id, "TechFlow SaaS", "techflow.io"))

    start_date = datetime.now() - timedelta(days=180)

    for i in range(num_teams):
        team_id = generate_uuid()
        
        # Generate a semi-realistic team name
        dept = random.choice(DEPARTMENTS)
        suffix = random.choice(TEAM_SUFFIXES)
        team_name = f"{dept} - {suffix} {random.randint(1, 99)}" # e.g., "Engineering - Core 42"
        
        cur.execute("INSERT INTO teams (id, name, organization_id) VALUES (?, ?, ?)",
                    (team_id, team_name, org_id))
        
        # Generate Projects for this team
        # Default to Engineering templates if department not found
        p_templates = PROJECT_TEMPLATES.get(dept, PROJECT_TEMPLATES["Engineering"])
        
        for _ in range(num_projects_per_team):
            p_id = generate_uuid()
            p_base_name = random.choice(p_templates)
            p_name = f"{p_base_name} - {random.choice(['Q1', 'Q2', 'Q3', 'Q4'])}"
            p_created = random_date(start_date, start_date + timedelta(days=60))
            
            cur.execute("""
                INSERT INTO projects (id, name, team_id, description, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (p_id, p_name, team_id, f"Project for {dept}", p_created))
            
            # Generate Sections
            section_ids = []
            for sec_name in SECTIONS:
                s_id = generate_uuid()
                cur.execute("INSERT INTO sections (id, name, project_id) VALUES (?, ?, ?)",
                            (s_id, sec_name, p_id))
                section_ids.append(s_id)
                
            generated_projects.append({
                "id": p_id, 
                "type": dept, # Pass the department to the task generator
                "sections": section_ids,
                "created_at": p_created
            })
            
    conn.commit()
    conn.close()
    return generated_projects