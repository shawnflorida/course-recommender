import random
import pandas as pd

def generate_professor_dataset(n=5000):
    qualifications = ['PhD', 'Masters', 'Bachelors']
    subjects = ['Computer Science', 'Information Technology']
    courses = {
        'Computer Science': ['Machine Learning', 'Data Science', 'Data Structures', 'Algorithms', 'Operating Systems', 'Cybersecurity', 'Artificial Intelligence', 'Software Engineering'],
        'Information Technology': ['Cloud Computing', 'Database Systems', 'Network Security', 'Web Development', 'Big Data', 'Blockchain', 'IT Project Management', 'IoT']
    }
    learning_styles = ['Workshop', 'Seminar', 'Bootcamp', 'One-on-One', 'Hands-on', 'Group Work']
    certifications = ['Google ML Cert', 'Azure Certification', 'Data Science Specialization', 'AI & Deep Learning', 'Certified Educator', 'AWS Cloud Cert', 'Cisco Network Cert', 'None']
    teaching_methods = ['Hands-on Projects', 'Lecture-based', 'Case Studies', 'Flipped Classroom']
    university_types = ['Open University', 'State University', 'Community College', 'Private University']
    genders = ['Male', 'Female', 'Non-Binary']
    
    data = []
    for _ in range(n):
        qualification = random.choice(qualifications)
        subject = random.choice(subjects)
        
        # Introduce correlation: Higher qualifications lead to more teaching years
        if qualification == 'PhD':
            teaching_years = random.randint(10, 30)
            age = teaching_years + random.randint(35, 60)
        elif qualification == 'Masters':
            teaching_years = random.randint(5, 20)
            age = teaching_years + random.randint(25, 45)
        else:
            teaching_years = random.randint(1, 10)
            age = teaching_years + random.randint(22, 35)
        
        taught_courses = random.sample(courses[subject], k=random.randint(2, 4))
        seminars_attended = random.sample([f'{s} in {subject}' for s in ['AI', 'Cybersecurity Trends', 'Cloud Innovations', 'Data Science']], k=random.randint(1, 3))
        research_interests = random.sample(courses[subject], k=random.randint(1, 2))
        
        # Introduce correlation: Certifications influence teaching methods
        certification = random.choice(certifications)
        if certification in ['Google ML Cert', 'AI & Deep Learning']:
            teaching_method = 'Hands-on Projects'
        elif certification in ['AWS Cloud Cert', 'Cisco Network Cert']:
            teaching_method = 'Case Studies'
        else:
            teaching_method = random.choice(teaching_methods)
        
        # Introduce correlation: Higher qualifications and certifications lead to better student performance
        if qualification == 'PhD' or certification != 'None':
            student_performance = round(random.uniform(3.0, 4.0), 2)
        else:
            student_performance = round(random.uniform(2.5, 3.5), 2)
        
        # Introduce correlation: Attendance positively affects student performance
        attendance = random.randint(50, 100)
        student_performance = min(4.0, student_performance + (attendance - 50) * 0.01)
        
        future_courses = random.sample(courses[subject], k=random.randint(1, 2))
        
        # Add new columns
        gender = random.choice(genders)
        university_type = random.choice(university_types)
        if qualification == 'PhD':
            publication_count = random.randint(5, 30)
        elif qualification == 'Masters':
            publication_count = random.randint(0, 15)
        else:
            publication_count = random.randint(0, 5)
        student_feedback_score = round(random.uniform(3.0, 5.0), 1)  # Scale of 1-5
        
        data.append([
            qualification, subject, teaching_years, student_performance, attendance,
            ', '.join(taught_courses), ', '.join(seminars_attended), ', '.join(research_interests),
            learning_styles, certification, teaching_method, ', '.join(future_courses),
            age, gender, university_type, publication_count, student_feedback_score
        ])
    
    df = pd.DataFrame(data, columns=[
        'Education Qualification', 'Subject Expertise', 'Teaching Years',
        'Student Performance', 'Attendance', 'Courses Previously Taught', 'Seminars Attended',
        'Research Interests', 'Learning Style', 'Certifications', 'Teaching Methodology', 'Future Courses',
        'Age', 'Gender', 'University Type', 'Publication Count', 'Student Feedback Score'
    ])
    return df

# Generate and display a sample dataset
dataset = generate_professor_dataset()
print(dataset.head())

# Save the DataFrame to a CSV file
dataset.to_csv('professor_dataset.csv', index=False)