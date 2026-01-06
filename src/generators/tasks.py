import random
from datetime import timedelta, datetime
from tqdm import tqdm
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date, is_weekend
from src.utils.llm_client import llm

def generate_tasks(projects, users, tasks_per_project):
    total_tasks = len(projects) * tasks_per_project
    print(f"Generating ~{total_tasks} tasks with realistic comments...")
    
    conn = get_connection()
    cur = conn.cursor()
    
    user_ids = [u['id'] for u in users]
    
    for proj in tqdm(projects, desc="Processing Projects"):
        for _ in range(tasks_per_project):
            t_id = generate_uuid()
            created_at = random_date(proj['created_at'], datetime.now())
            
            # 1. Determine Due Date
            days_to_complete = random.randint(1, 30)
            due_date = created_at + timedelta(days=days_to_complete)
            
            # Heuristic: Avoid weekend due dates
            if is_weekend(due_date):
                due_date += timedelta(days=2)
                
            # 2. Determine Completion Status
            is_completed = random.random() < 0.7
            completed_at = None
            if is_completed:
                offset = random.choice([-2, -1, 0, 0, 1, 5]) 
                completed_at = due_date + timedelta(days=offset)
                if completed_at < created_at:
                    completed_at = created_at + timedelta(hours=1)
                # Ensure we don't complete in the future
                if completed_at > datetime.now():
                    is_completed = False
                    completed_at = None

            # 3. Generate Content via Mock LLM
            name = llm.generate_task_name(proj['type'])
            desc = llm.generate_description()
            
            assignee = random.choice(user_ids) if random.random() > 0.1 else None
            section = random.choice(proj['sections'])
            
            # Insert Task
            cur.execute("""
                INSERT INTO tasks 
                (id, name, description, assignee_id, project_id, section_id, due_date, created_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (t_id, name, desc, assignee, proj['id'], section, due_date, created_at, is_completed, completed_at))
            
            # 4. Generate Realistic Comments
            # 50% chance of having comments
            if random.random() > 0.5:
                # Randomly 1 to 4 comments per task
                num_comments = random.randint(1, 4)
                
                # Comments must happen between Task Creation and Completion (or Now)
                comment_end_date = completed_at if completed_at else datetime.now()
                
                for _ in range(num_comments):
                    c_id = generate_uuid()
                    c_author = random.choice(user_ids)
                    
                    # Ensure comment timestamp is valid
                    if comment_end_date > created_at:
                        c_created = random_date(created_at, comment_end_date)
                    else:
                        c_created = created_at + timedelta(minutes=random.randint(5, 60))
                    
                    # NEW: Pass project type to get specific jargon
                    c_content = llm.generate_comment(proj['type'])
                    
                    cur.execute("INSERT INTO comments VALUES (?, ?, ?, ?, ?)",
                                (c_id, t_id, c_author, c_content, c_created))

    conn.commit()
    conn.close()