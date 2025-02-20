import pandas as pd
import random
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# Connect to SQLite database
engine = create_engine('sqlite:///university.db')

# Load existing data
teachers = pd.read_sql('SELECT teacher_id FROM teachers', engine)
seminars = pd.read_sql('SELECT seminar_id FROM seminars', engine)
specializations = pd.read_sql('SELECT specialization_id FROM specializations', engine)
activities = pd.read_sql('SELECT * FROM activities', engine)

# Generate at least 300 new rows
new_activities = []

for i in range(300):
    activity_id = f"A{len(activities) + len(new_activities) + 1:03}"
    teacher_id = random.choice(teachers['teacher_id'].tolist())
    seminar_id = random.choice(seminars['seminar_id'].tolist())
    specialization_id = random.choice(specializations['specialization_id'].tolist())
    activity_name = f"Activity {len(activities) + len(new_activities) + 1}"  # Unique activity name
    activity_date = datetime.today() - timedelta(days=random.randint(1, 365))

    new_activities.append((activity_id, teacher_id, seminar_id, specialization_id, None, None, activity_name, activity_date))

# Convert to DataFrame
new_activities_df = pd.DataFrame(new_activities, columns=[
    'activity_id', 'teacher_id', 'seminar_id', 'specialization_id', 'subject_id', 'course_id', 'activity_name', 'activity_date'
])

# Insert new activities into database
new_activities_df.to_sql('activities', engine, if_exists='append', index=False)

print("✅ Successfully added 300+ new activities!")
