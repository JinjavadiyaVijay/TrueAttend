import streamlit as st
from database.db import get_subject_by_code, enroll_student_to_subject
import time


@st.dialog("Enroll in Subject")
def enroll_dialog():
    """Enter a subject code to join a teacher's course."""
    st.write("Enter the subject code provided by your teacher to enroll.")
    join_code = st.text_input("Subject Code", placeholder="Eg. CS101")

    if st.button("Enroll Now", type="primary", width="stretch"):
        if not join_code or not join_code.strip():
            st.warning("Please enter a subject code.")
            return

        subject = get_subject_by_code(join_code.strip())
        if not subject:
            st.error("Subject not found. Check the code and try again.")
            return

        student_id = st.session_state.student_data['student_id']
        result = enroll_student_to_subject(student_id, subject['subject_id'])

        if result is None:
            st.warning("You are already enrolled in this subject.")
        else:
            st.toast(f"Enrolled in {subject['name']}!", icon="🎉")
            time.sleep(1)
            st.rerun()
