import pickle
import streamlit as st
import pandas as pd

# Load models
with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
    
with open('courses_model.pkl', 'rb') as f:
    courses_model = pickle.load(f)
with open('certifications_model.pkl', 'rb') as f:
    certifications_model = pickle.load(f)

# Load dataset
df = pd.read_csv('professor_dataset.csv')

# Streamlit UI Styling
st.set_page_config(page_title="Professor Recommender", page_icon="🎓", layout="wide")

# Custom CSS for Styling
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; }
        h1 { font-size: 40px; color: #007BFF; font-weight: bold; text-align: center; }
        .group-box { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        .stButton > button { background-color: #007BFF; color: white; padding: 12px 24px; font-size: 18px; border-radius: 10px; }
        .stButton > button:hover { background-color: #0056b3; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎓 Professor Course & Certification Recommender</h1>", unsafe_allow_html=True)
st.write("### Fill in the details to get personalized recommendations!")

# User Input Sections
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## 📚 **Education & Expertise**", unsafe_allow_html=True)
        with st.container():
            education = st.selectbox('**🎓 Education Qualification**', df['Education Qualification'].unique())
            subject = st.selectbox('**📖 Subject Expertise**', df['Subject Expertise'].unique())
            teaching_method = st.selectbox('**🧑‍🏫 Teaching Methodology**', df['Teaching Methodology'].unique())

        st.markdown("## 🎓 **Teaching & Research Background**", unsafe_allow_html=True)
        with st.container():
            courses_option = st.radio("**📘 Select or Enter Courses Previously Taught**", ["Select from List", "Enter Manually"])
            courses_taught = st.selectbox("**📗 Courses Previously Taught**", df["Courses Previously Taught"].dropna().unique()) if courses_option == "Select from List" else st.text_area("**📝 Enter Courses Previously Taught**")

            seminars_option = st.radio("**🎤 Select or Enter Seminars Attended**", ["Select from List", "Enter Manually"])
            seminars = st.selectbox("**📅 Seminars Attended**", df["Seminars Attended"].dropna().unique()) if seminars_option == "Select from List" else st.text_area("**📝 Enter Seminars Attended**")

            research_option = st.radio("**🔬 Select or Enter Research Interests**", ["Select from List", "Enter Manually"])
            research = st.selectbox("**🧪 Research Interests**", df["Research Interests"].dropna().unique()) if research_option == "Select from List" else st.text_area("**📝 Enter Research Interests**")

   

    
    
    with col2:
        st.markdown("### 📊 Additional Details", unsafe_allow_html=True)
        with st.container():
            age = st.number_input("Age", min_value=25, max_value=80, value=35)
            gender = st.radio("Gender", ["Male", "Female", "Other"])
            university_type = st.selectbox("University Type", df["University Type"].unique())
            publication_count = st.number_input("Publication Count", min_value=0, value=5)
            student_feedback = st.slider("Student Feedback Score", min_value=1.0, max_value=5.0, value=3.0, step=0.1)

import streamlit as st

st.markdown(
    """
    <style>
        .group-box {
            border: 2px solid #4CAF50;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        
        .group-box:hover {
            transform: scale(1.02);
            background-color: #fffde7;
        }
        
        h4 {
            color: #4CAF50;
            margin-bottom: 5px;
        }
        
        h2 {
            color: #333;
        }

        a {
            text-decoration: none;
            color: #007BFF;
            font-weight: bold;
            display: inline-block;
            margin-top: 5px;
            transition: color 0.3s;
        }

        a:hover {
            color: #ffcc00;
        }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("🔮 Predict Future Courses & Certifications"):
    user_input = f"{education} {subject} {courses_taught} {seminars} {research} {teaching_method} {age} {gender} {university_type} {publication_count} {student_feedback}"
    user_vector = vectorizer.transform([user_input])

    future_courses_pred = courses_model.predict(user_vector)[0]
    certifications_pred = certifications_model.predict(user_vector)[0]

    st.success("✅ Predictions Generated Successfully!")

    # Convert to Coursera search links
    future_courses_link = f"https://www.coursera.org/search?query={future_courses_pred.replace(' ', '-')}"
    certifications_link = f"https://www.coursera.org/search?query={certifications_pred.replace(' ', '-')}"

    # Grouped Predictions Display
    st.markdown("### 🔍 Recommended Courses & Certifications", unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
                <div class='group-box'>
                    <h6>📘 Recommended Future Course</h6>
                    <h1>{future_courses_pred}</h1>
                    <a href="{future_courses_link}" target="_blank">🔗 View on Coursera</a>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='group-box'>
                    <h6>🎖️ Recommended Certification</h6>
                    <h1>{certifications_pred}</h1>
                    <a href="{certifications_link}" target="_blank">🔗 View on Coursera</a>
                </div>
            """, unsafe_allow_html=True)
