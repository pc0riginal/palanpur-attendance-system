import pandas as pd
import random
from faker import Faker
from datetime import datetime

# Initialize Faker
fake = Faker("en_IN")

# Define categories
sabha_types = ["Bal", "Yuvak", "Mahila", "Sanyukt"]
age_groups = ["5-12", "13-25", "26-35", "36-50", "51-65", "65+"]

records = []

def generate_phone():
    """Generate a valid 10-digit Indian phone number."""
    start_digit = random.choice(["6", "7", "8", "9"])
    remaining = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return start_digit + remaining

# Generate 500 random devotee records
for _ in range(500):
    name = fake.name()
    contact_number = generate_phone()
    sabha_type = random.choice(sabha_types)
    photo_url = f"https://lh3.googleusercontent.com/pw/{fake.sha1()}"
    age_group = random.choice(age_groups)
    address = fake.city()
    join_date = fake.date_between(start_date="-2y", end_date="today").strftime("%d/%m/%Y")
    
    records.append({
        "name": name,
        "contact_number": contact_number,
        "sabha_type": sabha_type,
        "photo_url": photo_url,
        "age_group": age_group,
        "address": address,
        "join_date": join_date
    })

# Create DataFrame
df = pd.DataFrame(records)

# Save to Excel
df.to_excel("devotee_data.xlsx", index=False)

print("✅ Excel file 'devotee_data.xlsx' created successfully with 500 records and valid 10-digit phone numbers.")
