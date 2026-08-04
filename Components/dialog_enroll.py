import time

import streamlit as st

from database.db import (
    enroll_student_to_subject,
    get_student_subjects,
    get_subject_by_code,
)


PENDING_JOIN_CODE_KEY = "pending_join_code"


def _clear_join_code():
    st.query_params.clear()
    st.session_state.pop(PENDING_JOIN_CODE_KEY, None)


def _student_already_enrolled(student_id, subject_id):
    enrollments = get_student_subjects(student_id)
    return any(
        enrollment.get("subject_id") == subject_id
        or (enrollment.get("subjects") or {}).get("subject_id") == subject_id
        for enrollment in enrollments
    )


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

        student_id = st.session_state.student_data["student_id"]
        result = enroll_student_to_subject(student_id, subject["subject_id"])

        if result is None:
            st.warning("You are already enrolled in this subject.")
        else:
            st.toast(f"Enrolled in {subject['name']}!", icon="🎉")
            time.sleep(1)
            st.rerun()


@st.dialog("Quick Enroll in Subject")
def auto_enroll_dialog(subject_code):
    subject_code = subject_code.strip() if subject_code else ""
    student = st.session_state.get("student_data")

    if not student:
        st.info("Please log in as a student to join this subject.")
        return

    subject = get_subject_by_code(subject_code)
    if not subject:
        st.error("Subject not found. Check the invitation link and try again.")
        if st.button("Close"):
            _clear_join_code()
            st.rerun()
        return

    student_id = student["student_id"]
    subject_id = subject["subject_id"]

    if _student_already_enrolled(student_id, subject_id):
        st.info(f"You are already enrolled in {subject['name']}.")
        if st.button("Got it", type="primary"):
            _clear_join_code()
            st.rerun()
        return

    st.markdown(f"Would you like to enroll in **{subject['name']}**?")
    st.caption(f"Subject code: {subject['subject_code']}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("No thanks"):
            _clear_join_code()
            st.rerun()
    with col2:
        if st.button("Yes, enroll now", type="primary", width="stretch"):
            result = enroll_student_to_subject(student_id, subject_id)
            if result is None:
                st.info(f"You are already enrolled in {subject['name']}.")
            else:
                st.success(f"Joined {subject['name']} successfully!")
            _clear_join_code()
            time.sleep(1)
            st.rerun()
