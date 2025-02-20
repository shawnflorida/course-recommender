import streamlit as st
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv('professor_dataset.csv')

# Convert all non-target columns into a single text feature
target_columns = ['Future Courses', 'Certifications']
df = df.dropna(subset=target_columns)  # Remove rows with missing target values

# Convert all columns except target variables into strings and concatenate them
feature_columns = [col for col in df.columns if col not in target_columns]
df['combined_text'] = df[feature_columns].astype(str).apply(lambda x: ' '.join(x.dropna()), axis=1)

# Train TF-IDF model
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['combined_text'])

# Train Future Courses Model
X_train, X_test, y_train, y_test = train_test_split(X, df['Future Courses'], test_size=0.2, random_state=42)

courses_model = RandomForestClassifier(n_estimators=100, random_state=42)
courses_model.fit(X_train, y_train)

# Train Certifications Model
X_train, X_test, y_train, y_test = train_test_split(X, df['Certifications'], test_size=0.2, random_state=42)

certifications_model = RandomForestClassifier(n_estimators=100, random_state=42)
certifications_model.fit(X_train, y_train)

# Save models
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
with open('courses_model.pkl', 'wb') as f:
    pickle.dump(courses_model, f)
with open('certifications_model.pkl', 'wb') as f:
    pickle.dump(certifications_model, f)
