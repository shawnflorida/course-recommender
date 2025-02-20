import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('university.db')
c = conn.cursor()

# Create Tables
c.executescript('''
CREATE TABLE IF NOT EXISTS courses (
    course_id TEXT PRIMARY KEY,
    course_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id TEXT PRIMARY KEY,
    course_id TEXT,
    subject_name TEXT UNIQUE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE IF NOT EXISTS specializations (
    specialization_id TEXT PRIMARY KEY,
    subject_id TEXT,
    specialization_name TEXT UNIQUE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
);

CREATE TABLE IF NOT EXISTS seminars (
    seminar_id TEXT PRIMARY KEY,
    seminar_name TEXT,
    specialization_id TEXT,
    seminar_education_level TEXT,
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id)
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id TEXT PRIMARY KEY,
    name TEXT,
    education TEXT,
    specialization_expertise TEXT,
    university_type TEXT,
    gender TEXT,
    age INTEGER,
    publications_count INTEGER,
    FOREIGN KEY (specialization_expertise) REFERENCES specializations(specialization_id)
);

CREATE TABLE IF NOT EXISTS activities (
    activity_id TEXT PRIMARY KEY,
    activity_name TEXT,
    activity_date TEXT,
    teacher_id TEXT,
    seminar_id TEXT,
    specialization_id TEXT,
    subject_id TEXT,
    course_id TEXT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
    FOREIGN KEY (seminar_id) REFERENCES seminars(seminar_id),
    FOREIGN KEY (specialization_id) REFERENCES specializations(specialization_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
''')

# Insert Data
courses = [
    ('IT101', 'Information Technology'),
    ('CS101', 'Computer Science')
]
c.executemany("INSERT INTO courses VALUES (?, ?) ON CONFLICT(course_id) DO NOTHING;", courses)

subjects = [
    ('ITDB', 'IT101', 'Database Management'),
    ('ITNW', 'IT101', 'Networking'),
    ('ITCY', 'IT101', 'Cybersecurity'),
    ('CSDT', 'CS101', 'Data Structures'),
    ('CSAL', 'CS101', 'Algorithms'),
    ('CSAI', 'CS101', 'Artificial Intelligence'),
    ('CSML', 'CS101', 'Machine Learning'),
    ('CSDV', 'CS101', 'Data Visualization')
]
c.executemany("INSERT INTO subjects VALUES (?, ?, ?) ON CONFLICT(subject_id) DO NOTHING;", subjects)

specializations = [
    ('ITCC', 'ITDB', 'Cloud Computing'),
    ('ITNS', 'ITCY', 'Network Security'),
    ('CSDS', 'CSAI', 'Data Science'),
    ('CSML', 'CSML', 'Machine Learning'),
    ('CSDV', 'CSDV', 'Data Visualization'),
    ('CSSE', 'CSAL', 'Software Engineering')
]
c.executemany("INSERT INTO specializations VALUES (?, ?, ?) ON CONFLICT(specialization_id) DO NOTHING;", specializations)

seminars = [
    ('ITCCS', 'Cloud Security', 'ITCC', 'Advanced'),
    ('ITNSE', 'Ethical Hacking', 'ITNS', 'Intermediate'),
    ('CSMLD', 'Deep Learning', 'CSML', 'Advanced'),
    ('CSSEA', 'Agile Development', 'CSSE', 'Intermediate'),
    ('CSDSA', 'Data Science Applications', 'CSDS', 'Beginner'),
    ('CSDVT', 'Data Visualization Techniques', 'CSDV', 'Beginner'),
    ('ITCCS', 'Cloud Computing Fundamentals', 'ITCC', 'Beginner'),
    ('ITCCS', 'Serverless Architecture', 'ITCC', 'Advanced'),
    ('ITNSE', 'Penetration Testing Strategies', 'ITNS', 'Advanced'),
    ('ITNSE', 'Cyber Forensics & Investigation', 'ITNS', 'Intermediate'),
    ('CSMLD', 'Reinforcement Learning Basics', 'CSML', 'Advanced'),
    ('CSMLD', 'Natural Language Processing', 'CSML', 'Intermediate'),
    ('CSSEA', 'Software Development Lifecycle', 'CSSE', 'Beginner'),
    ('CSSEA', 'Microservices and DevOps', 'CSSE', 'Advanced'),
    ('CSDSA', 'Big Data Analytics', 'CSDS', 'Advanced'),
    ('CSDSA', 'AI in Healthcare', 'CSDS', 'Intermediate'),
    ('CSDVT', 'Storytelling with Data', 'CSDV', 'Beginner'),
    ('CSDVT', 'Interactive Dashboards', 'CSDV', 'Intermediate'),
    ('CSDBA', 'SQL Optimization & Indexing', 'CSDB', 'Advanced'),
    ('CSDBA', 'NoSQL Databases Overview', 'CSDB', 'Beginner'),
    ('CSNET', 'Cybersecurity in 5G Networks', 'CSNT', 'Advanced'),
    ('CSNET', 'Network Automation with Python', 'CSNT', 'Intermediate'),
    ('CSALD', 'Advanced Algorithms', 'CSAL', 'Advanced'),
    ('CSALD', 'Graph Theory & Applications', 'CSAL', 'Intermediate'),
    ('ITCCS', 'Hybrid Cloud Deployments', 'ITCC', 'Intermediate'),
    ('ITNSE', 'Zero Trust Security Model', 'ITNS', 'Advanced'),
    ('CSDSA', 'Predictive Analytics', 'CSDS', 'Advanced'),
    ('CSMLD', 'Transformers & LLMs', 'CSML', 'Advanced'),
    ('CSDVT', 'Geospatial Data Visualization', 'CSDV', 'Advanced'),
    ('CSSEA', 'Blockchain for Business', 'CSSE', 'Beginner'),
    ('CSDBA', 'Distributed Database Systems', 'CSDB', 'Advanced'),
    ('CSNET', 'IoT Security & Risk Management', 'CSNT', 'Intermediate'),
    ('CSDSA', 'Recommender Systems', 'CSDS', 'Advanced'),
    ('CSMLD', 'Autonomous AI Systems', 'CSML', 'Advanced'),
    ('CSALD', 'Bioinformatics Algorithms', 'CSAL', 'Intermediate'),
    ('ITCCS', 'Cloud Networking Principles', 'ITCC', 'Intermediate'),
    ('ITNSE', 'Incident Response Planning', 'ITNS', 'Advanced'),
    ('CSDBA', 'Data Warehousing Strategies', 'CSDB', 'Intermediate'),
    ('CSSEA', 'Version Control Best Practices', 'CSSE', 'Beginner'),
    ('CSMLD', 'AI Ethics & Bias Mitigation', 'CSML', 'Intermediate'),
    ('CSDVT', 'AR & VR Data Visualization', 'CSDV', 'Advanced'),
    ('CSDSA', 'Edge Computing Analytics', 'CSDS', 'Advanced')
]

c.executemany("INSERT INTO seminars VALUES (?, ?, ?, ?) ON CONFLICT(seminar_id) DO NOTHING;", seminars)

teachers = [
    ('T001', 'Alice Johnson', 'PhD IT', 'ITCC', 'Public', 'F', 45, 10),
    ('T002', 'Bob Smith', 'MSc IT', 'ITCC', 'Private', 'M', 38, 7),
    ('T003', 'Charlie Brown', 'PhD IT', 'ITNS', 'Public', 'M', 50, 12),
    ('T004', 'Diana King', 'MSc IT', 'ITNS', 'Private', 'F', 42, 9),
    ('T005', 'Ethan Clark', 'PhD IT', 'ITCC', 'Public', 'M', 48, 11),
    ('T006', 'Fiona Lee', 'PhD CS', 'CSML', 'Public', 'F', 46, 13),
    ('T007', 'George Adams', 'MSc CS', 'CSML', 'Private', 'M', 40, 8),
    ('T008', 'Hannah Wright', 'PhD CS', 'CSSE', 'Public', 'F', 44, 10),
    ('T009', 'Ian Turner', 'MSc CS', 'CSSE', 'Private', 'M', 39, 7),
    ('T010', 'Jack Evans', 'PhD CS', 'CSML', 'Public', 'M', 47, 11),
    ('T011', 'Karen White', 'PhD CS', 'CSDS', 'Public', 'F', 43, 14),
    ('T012', 'Liam Green', 'MSc CS', 'CSDV', 'Private', 'M', 37, 6)
]
c.executemany("INSERT INTO teachers VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(teacher_id) DO NOTHING;", teachers)
activities = [
    ('A001', 'Cloud Security Workshop', '2025-02-15', 'T001', 'ITCCS', 'ITCC', 'ITDB', 'IT101'),
    ('A002', 'Advanced Networking Seminar', '2025-03-10', 'T001', 'ITCCS', 'ITCC', 'ITNW', 'IT101'),
    ('A003', 'Cybersecurity Essentials', '2025-04-05', 'T002', 'ITCCS', 'ITCC', 'ITCY', 'IT101'),
    ('A004', 'Ethical Hacking Basics', '2025-05-20', 'T003', 'ITNSE', 'ITNS', 'ITDB', 'IT101'),
    ('A005', 'Network Security Advanced', '2025-06-15', 'T003', 'ITNSE', 'ITNS', 'ITNW', 'IT101'),
    ('A006', 'Cyber Defense Strategies', '2025-07-10', 'T004', 'ITNSE', 'ITNS', 'ITCY', 'IT101'),
    ('A007', 'Cloud Infrastructure Management', '2025-08-25', 'T005', 'ITCCS', 'ITCC', 'ITDB', 'IT101'),
    ('A008', 'Networking in Cloud Environments', '2025-09-30', 'T005', 'ITCCS', 'ITCC', 'ITNW', 'IT101'),
    ('A009', 'Deep Learning Techniques', '2025-10-15', 'T006', 'CSMLD', 'CSML', 'CSDT', 'CS101'),
    ('A010', 'Machine Learning Applications', '2025-11-05', 'T006', 'CSMLD', 'CSML', 'CSML', 'CS101'),
    ('A011', 'Data Visualization Workshop', '2025-12-10', 'T007', 'CSDVT', 'CSDV', 'CSDV', 'CS101'),
    ('A012', 'Big Data Analytics', '2026-01-20', 'T011', 'CSDSA', 'CSDS', 'CSDS', 'CS101'),
    ('A013', 'AI in Healthcare', '2026-02-15', 'T011', 'CSDSA', 'CSDS', 'CSDS', 'CS101'),
    ('A014', 'Reinforcement Learning Basics', '2026-03-10', 'T010', 'CSMLD', 'CSML', 'CSML', 'CS101'),
    ('A015', 'Software Engineering Best Practices', '2026-04-25', 'T008', 'CSSEA', 'CSSE', 'CSAL', 'CS101'),
    ('A016', 'Blockchain for Business', '2026-05-30', 'T008', 'CSSEA', 'CSSE', 'CSSE', 'CS101'),
    ('A017', 'Penetration Testing Strategies', '2026-06-20', 'T003', 'ITNSE', 'ITNS', 'ITCY', 'IT101'),
    ('A018', 'Cyber Forensics & Investigation', '2026-07-15', 'T004', 'ITNSE', 'ITNS', 'ITCY', 'IT101'),
    ('A019', 'Graph Theory & Applications', '2026-08-10', 'T009', 'CSALD', 'CSAL', 'CSAL', 'CS101'),
    ('A020', 'Agile Development in Practice', '2026-09-05', 'T008', 'CSSEA', 'CSSE', 'CSSE', 'CS101'),
    ('A021', 'IoT Security & Risk Management', '2026-10-12', 'T012', 'CSNET', 'CSNT', 'CSNT', 'CS101'),
    ('A022', 'Predictive Analytics', '2026-11-18', 'T011', 'CSDSA', 'CSDS', 'CSDS', 'CS101'),
    ('A023', 'Transformers date& LLMs', '2026-12-22', 'T010', 'CSMLD', 'CSML', 'CSML', 'CS101'),
    ('A024', 'Cloud Networking Principles', '2027-01-10', 'T005', 'ITCCS', 'ITCC', 'ITDB', 'IT101'),
    ('A025', 'Incident Response Planning', '2027-02-15', 'T004', 'ITNSE', 'ITNS', 'ITCY', 'IT101'),
    ('A026', 'Data Warehousing Strategies', '2027-03-20', 'T012', 'CSDBA', 'CSDB', 'CSDB', 'CS101'),
    ('A027', 'Version Control Best Practices', '2027-04-15', 'T008', 'CSSEA', 'CSSE', 'CSSE', 'CS101'),
    ('A028', 'AI Ethics & Bias Mitigation', '2027-05-05', 'T006', 'CSMLD', 'CSML', 'CSML', 'CS101'),
    ('A029', 'AR & VR Data Visualization', '2027-06-10', 'T007', 'CSDVT', 'CSDV', 'CSDV', 'CS101'),
    ('A030', 'Edge Computing Analytics', '2027-07-15', 'T011', 'CSDSA', 'CSDS', 'CSDS', 'CS101')
]

c.executemany(
    "INSERT INTO activities (activity_id, activity_name, activity_date, teacher_id, seminar_id, specialization_id, subject_id, course_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(activity_id) DO NOTHING;",
    activities
)
# Commit and close
conn.commit()
conn.close()