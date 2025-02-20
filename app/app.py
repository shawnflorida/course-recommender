import sqlite3
import time
import streamlit as st
import pandas as pd
import random
from sqlalchemy import create_engine
from datetime import date

# Connect to SQLite database
engine = create_engine('sqlite:///university.db')

# Fetch data from the database
def load_data():
    teachers = pd.read_sql('SELECT * FROM teachers', engine)
    activities = pd.read_sql('SELECT * FROM activities', engine)
    specializations = pd.read_sql('SELECT * FROM specializations', engine)
    seminars = pd.read_sql("SELECT * FROM seminars", engine)
    subjects = pd.read_sql("SELECT * FROM subjects", engine)
    courses = pd.read_sql("SELECT * FROM courses", engine)
    df = pd.read_sql("SELECT * FROM specializations", sqlite3.connect("university.db"))
    print(df)
    return teachers, activities, seminars, specializations, subjects, courses

# Display teacher information
def display_teacher_info(teacher):
    st.markdown(f"""
        <h2 style='color:#4B8BBE;'>{teacher['name']}</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**🎓 Education:** {teacher['education']}")
        st.write(f"**🏫 University Type:** {teacher['university_type']}")
        st.write(f"**📅 Age:** {teacher['age']}")
    with col2:
        st.write(f"**⚥ Gender:** {teacher['gender']}")
        st.write(f"**📚 Publications:** {teacher['publications_count']}")

# Display current specialization
def display_current_specialization(teacher, specializations):
    specialization = specializations[specializations['specialization_id'] == teacher['specialization_expertise']]
    if not specialization.empty:
        with st.expander("📌 **Current Specialization**"):
            st.markdown(f"### 🎯 {specialization.iloc[0]['specialization_name']}")
            # Display recent activities
def display_recent_activities(teacher, activities, seminars):
    st.subheader("📝 Recent Activities")
    
    # Filter activities for the selected teacher
    teacher_activities = activities[activities['teacher_id'] == teacher['teacher_id']]
    
    if not teacher_activities.empty:
        # Merge with seminar names
        merged_activities = teacher_activities.merge(seminars[['seminar_id', 'seminar_name']], on='seminar_id', how='left')

        # Display as table
        st.table(merged_activities[['activity_name', 'activity_date']]
             .rename(columns={'activity_name': '📌 Activity', 'activity_date': '📅 Date'}))
    else:
        st.info("No recent activities found.")

def add_activity(teacher, activities, seminars, specializations, engine):
            with st.expander("➕ **Add New Activity**"):
                # Select seminar
                seminar_names = seminars['seminar_name'].tolist()
                
                # Select specialization (dropdown)
                specialization_names = specializations['specialization_name'].tolist()
                specialization_options = ['None'] + specialization_names  
                selected_specialization = st.selectbox("🎯 **Select a Specialization (Optional)**", specialization_options)

                # Fetch specialization_id if a specialization is selected
                specialization_id = None
                if selected_specialization != "None":
                    specialization_row = specializations.loc[specializations['specialization_name'] == selected_specialization]
                    if not specialization_row.empty:
                        specialization_id = specialization_row['specialization_id'].values[0]

                # Select teacher
               
                teacher_id = teacher['teacher_id']

                # Enter activity details
                activity_name = st.text_input("📝 **Activity Name**")
                activity_date = st.date_input("📅 **Activity Date**", date.today())

                if st.button("✅ **Add Activity**"):
                    new_activity_id = f"A{len(activities) + 1:03}"

                    # Create new activity DataFrame
                    new_activity = pd.DataFrame({
                        'activity_id': [new_activity_id],
                        'teacher_id': [teacher_id],
                        'specialization_id': [specialization_id],  # Can be None if no specialization is selected
                        'activity_name': [activity_name],
                        'activity_date': [activity_date]
                    })

                    print(new_activity)

                    # Save to database
                    with engine.connect() as connection:
                        new_activity.to_sql('activities', connection, if_exists='append', index=False)
                        connection.commit()  # ✅ Explicit commit

                    # ✅ Update activities DataFrame immediately
                    updated_activities = pd.read_sql("SELECT * FROM activities", engine)

                    # ✅ Update session state so it refreshes without reloading
                    st.session_state['activities'] = updated_activities

                    st.success("🎉 **Activity added successfully!**")
                    time.sleep(2)  # Wait for 2 seconds
                    st.rerun()  # ✅ Force UI refresh
# Function to update specialization in the database
def update_specialization_in_db(teacher_id, specialization_name, conn):
    cursor = conn.cursor()
    
    # Fetch specialization ID based on name
    cursor.execute("SELECT specialization_id FROM specializations WHERE specialization_name = ?", (specialization_name,))
    specialization_id = cursor.fetchone()
    
    if specialization_id:
        specialization_id = specialization_id[0]
        
        # Update the teacher's specialization
        cursor.execute("UPDATE teachers SET specialization_expertise = ? WHERE teacher_id = ?", (specialization_id, teacher_id))
        conn.commit()
        cursor.execute("UPDATE teachers SET specialization_expertise = ? WHERE teacher_id = ?", (specialization_id, teacher_id))
        conn.commit()
        return True
    return False
    # Function to display TF-IDF suggested specialization and update it
def display_tfidf_suggestion(specializations, activities, teacher_id):
    st.markdown("*Based on your recent activities, this is what we recommend:*")
    
    with st.expander("💡 **TF-IDF Suggested Specialization**"):
        # Store the suggested specialization in session state
        if 'suggested_specialization' not in st.session_state:
            st.session_state['suggested_specialization'] = random.choice(specializations['specialization_name'].unique().tolist())
            st.rerun()  # ✅ Force UI refresh
        suggested_spec = st.session_state['suggested_specialization']
        st.markdown(f"### 🎯 Suggested Specialization: {suggested_spec}")

        # Fetch specialization UID instead of just ID (to get all related specializations)
        spec_uids = specializations.loc[specializations['specialization_name'] == suggested_spec, 'specialization_id'].tolist()
        
        if spec_uids:
            # Get **all** activities where specialization UID matches (not just exact spec_id)
            all_activities = activities[activities['specialization_id'].isin(spec_uids)]

            if not all_activities.empty:
                st.table(all_activities[['activity_name', 'activity_date']]
                         .rename(columns={'activity_name': '📌 Activity', 
                                          'activity_date': '📅 Activity Date'}).reset_index(drop=True))
            else:
                st.info("No activities found for this specialization UID.")
        else:
            st.warning("⚠️ Specialization UID not found.")
         # Button to generate another specialization
        if st.button("🔄 Generate Another Specialization"):
            st.session_state['suggested_specialization'] = random.choice(specializations['specialization_name'].unique().tolist())
            st.rerun()  # ✅ Force UI refresh
        # Display available specializations and allow user to pick a different one
        st.markdown("### 📋 Change Specialization")
        specialization_list = specializations['specialization_name'].unique().tolist()
        
        # Get index safely, defaulting to 0 if suggested_spec is not found
        selected_specialization = st.selectbox("🔽 Pick a different specialization if you prefer:", 
                                               specialization_list, 
                                               index=specialization_list.index(suggested_spec) if suggested_spec in specialization_list else 0)
        
        # Update specialization only if a new one is chosen
        if selected_specialization != suggested_spec:
            st.session_state['suggested_specialization'] = selected_specialization
        # Database connection
        conn = sqlite3.connect("university.db")  # Change to your actual database connection
        if st.button("👍 Make this my specialization!"):
            success = update_specialization_in_db(teacher_id, selected_specialization, conn)
            conn.close()  # Close connection

            if success:
                st.success(f"Great! You have chosen: **{selected_specialization}** and it has been updated in the database. ✅")
                time.sleep(2)  # Wait for 2 seconds
                st.rerun()  # ✅ Force UI refresh
            else:
                st.error("❌ Unable to update specialization. Please try again.")


def main():
    # Database connection
    DATABASE_URL = "sqlite:///university.db"  # Change this to your actual DB
    engine = create_engine(DATABASE_URL)
    st.markdown("""
        <style>
            .sidebar-button {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                margin: 5px 0;
                border: none;
                width: 100%;
                text-align: left;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
                border-radius: 5px;
            }
            .sidebar-button:hover {
                background-color: #45a049;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='color:#4B8BBE;'>📘 Faculty Information System</h1>", unsafe_allow_html=True)

    teachers, activities, seminars, specializations, subjects, courses  = load_data()
    
    st.sidebar.subheader("👩‍🏫 **Select a Teacher**")

    teacher_names = teachers["name"].tolist()
    selected_teacher_name = st.sidebar.selectbox("Choose a teacher", ["Select"] + teacher_names)

    if selected_teacher_name != "Select":
        selected_teacher = teachers[teachers["name"] == selected_teacher_name].iloc[0]
        st.session_state['selected_teacher'] = selected_teacher
    else:
        selected_teacher = None

    if 'selected_teacher' in st.session_state:
        selected_teacher = st.session_state['selected_teacher']
        
    
    teacher = selected_teacher
    if selected_teacher is not None:
        display_teacher_info(selected_teacher)
        display_current_specialization(selected_teacher, specializations)
        display_recent_activities(selected_teacher, activities, seminars)
        display_tfidf_suggestion(specializations,activities, selected_teacher['teacher_id'])
        add_activity(teacher, activities, seminars, specializations, engine)

    if selected_teacher is None:
        st.info("👈 Select a teacher from the dropdown to view details.")   

if __name__ == "__main__":
    main()
