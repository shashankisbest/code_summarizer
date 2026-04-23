import json
from typing import List, Dict

def parse_json(data: str) -> Dict:
    """Parse JSON string and return dictionary."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}

def filter_users(users: List[Dict], age_min: int) -> List[Dict]:
    """Filter users by minimum age."""
    return [user for user in users if user.get('age', 0) >= age_min]

data = '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]'
users = parse_json(data)
filtered = filter_users(users, 28)
print(filtered)
