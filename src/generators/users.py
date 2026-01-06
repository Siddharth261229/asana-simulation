from faker import Faker
from datetime import datetime, timedelta
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
import random

fake = Faker()

def generate_users(count):
    users = []
    print(f"Generating {count} users with realistic join dates...")
    
    # Realistic roles distribution
    roles = ["Admin", "Member", "Guest"]
    weights = [5, 90, 5]
    
    # Define the hiring window (e.g., company started hiring 3 years ago)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 3) # 3 years back
    
    for _ in range(count):
        # Generate a join date between 3 years ago and today
        join_date = random_date(start_date, end_date)
        
        user = {
            "id": generate_uuid(),
            "name": fake.name(),
            "email": fake.unique.company_email(),
            "role": random.choices(roles, weights=weights)[0],
            "created_at": join_date  # <--- NEW FIELD
        }
        users.append(user)
        
    conn = get_connection()
    cur = conn.cursor()
    
    # Updated SQL to include created_at
    cur.executemany(
        """
        INSERT INTO users (id, name, email, role, created_at) 
        VALUES (:id, :name, :email, :role, :created_at)
        """,
        users
    )
    conn.commit()
    conn.close()
    return users