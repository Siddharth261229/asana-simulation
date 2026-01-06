import random
from datetime import timedelta, datetime
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date, is_weekend
from src.utils.llm_client import llm

def generate_tasks(projects, users, tasks_per_project):
    print(f"Generating tasks (~{len(projects) * tasks_per_project})...")
    conn = get_connection()
    cur = conn.cursor()
    
    user_ids = [u['id'] for u in users]
    
    for proj in projects:
        for _ in range(tasks_per_project):
            t_id = generate_uuid()
            created_at = random_date(proj['created_at'], datetime.now())
            
            # 1. Determine Due Date
            days_to_complete = random.randint(1, 30)
            due_date = created_at + timedelta(days=days_to_complete)
            
            # 2. Heuristic: Avoid weekend due dates
            if is_weekend(due_date):
                due_date += timedelta(days=2)
                
            # 3. Determine Completion Status
            is_completed = random.random() < 0.7  # 70% completion rate
            completed_at = None
            if is_completed:
                # Most tasks completed near due date
                offset = random.choice([-2, -1, 0, 0, 1, 5]) # Days relative to due date
                completed_at = due_date + timedelta(days=offset)
                if completed_at < created_at:
                    completed_at = created_at + timedelta(hours=1)
                if completed_at > datetime.now():
                    is_completed = False
                    completed_at = None

            # 4. Generate Content via Mock LLM
            name = llm.generate_task_name(proj['type'])
            desc = llm.generate_description()
            
            # 5. Assignee (Zipfian distribution logic simplified)
            assignee = random.choice(user_ids) if random.random() > 0.1 else None
            section = random.choice(proj['sections'])
            
            cur.execute("""
                INSERT INTO tasks 
                (id, name, description, assignee_id, project_id, section_id, due_date, created_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (t_id, name, desc, assignee, proj['id'], section, due_date, created_at, is_completed, completed_at))
            
            # Generate Comments
            if random.random() > 0.5:
                num_comments = random.randint(1, 3)
                for _ in range(num_comments):
                    c_id = generate_uuid()
                    c_author = random.choice(user_ids)
                    c_created = random_date(created_at, completed_at if completed_at else datetime.now())
                    c_content = "Looking into this now." if random.random() > 0.5 else "Any updates?"
                    
                    cur.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?)",
                                (c_id, t_id, c_author, c_content, c_created))

    conn.commit()
    conn.close()