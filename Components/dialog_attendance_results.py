import streamlit as st
from database.db import create_attendance
import pandas as pd


@st.dialog("Attendance Results", width="large")
def attendance_result_dialog(subject_id, subject_name, results_df, logs):
    """
    Shows detected attendance for review before saving.
    results_df: DataFrame with columns [Name, Status]
    logs: list of dicts with keys: student_id, is_present
    """
    st.markdown('<h3 style="color:white; margin-top:0;">📋 ' + subject_name + '</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color:white; margin-bottom:10px;">Please review attendance before confirming.</p>', unsafe_allow_html=True)
    
    # Inject CSS specific to this dialog to fix colors
    st.markdown("""
        <style>
            div[role="dialog"] {
                color: white !important;
            }
            div[role="dialog"] h1, div[role="dialog"] h2, div[role="dialog"] h3, div[role="dialog"] p, div[role="dialog"] span, div[role="dialog"] div {
                color: white !important;
            }
            /* Fix button text inside this dialog */
            div[role="dialog"] button p {
                color: white !important;
            }
        </style>
    """, unsafe_allow_html=True)

    present_count = sum(1 for l in logs if l['is_present'])
    absent_count = len(logs) - present_count

    mc1, mc2, mc3 = st.columns(3)
    with mc1:
        st.metric("Total Students", len(logs))
    with mc2:
        st.metric("Present", present_count)
    with mc3:
        st.metric("Absent", absent_count)

    st.dataframe(results_df, hide_index=True, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('✅ Confirm & Save', type='primary', width='stretch'):
            with st.spinner("Saving attendance..."):
                try:
                    create_attendance(subject_id, logs)
                    st.toast("Attendance saved successfully!", icon="✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save: {str(e)}")

    with col2:
        if st.button('❌ Discard', width='stretch'):
            st.rerun()
