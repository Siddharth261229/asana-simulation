from faker import Faker
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid
import random

fake = Faker()

def generate_users(count):
    users = []
    print(f"Generating {count} users...")
    
    # Realistic roles distribution
    roles = ["Admin", "Member", "Guest"]
    weights = [5, 90, 5]
    
    for _ in range(count):
        user = {
            "id": generate_uuid(),
            "name": fake.name(),
            "email": fake.unique.company_email(),
            "role": random.choices(roles, weights=weights)[0]
        }
        users.append(user)
        
    conn = get_connection()
    cur = conn.cursor()
    cur.executemany(
        "INSERT INTO users (id, name, email, role) VALUES (:id, :name, :email, :role)",
        users
    )
    conn.commit()
    conn.close()
    return users