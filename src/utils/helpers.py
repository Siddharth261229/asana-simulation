import uuid
from datetime import datetime, timedelta
import random

def generate_uuid():
    return str(uuid.uuid4())

def random_date(start, end):
    if end <= start:
        end = start + timedelta(minutes=5)
    delta = end - start
    int_delta = int(delta.total_seconds())
    return start + timedelta(seconds=random.randrange(int_delta))

def is_weekend(dt):
    return dt.weekday() >= 5