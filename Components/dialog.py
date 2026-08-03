import streamlit as st
from database.db import create_subject

@st.dialog("Create New Subject")
def create_subject_dailog(teacher_id):
    st.write('Enter the details of new subjecr')
    sub_id = st.text_input("Subject Code",placeholder="C5101")
    sub_name = st.text_input("Subject None",placeholder="Introduction to Computer science")
    sub_section = st.text_input("Section",placeholder="A")
    
    if st.button("Create Subject Now",type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject Created")
                st.rerun()
            except Exception as e:
                st.error(f"Error{str(e)}")
        else:
            st.warning("Please fill all the fields")

@st.dialog("Share Subject Code")
def share_subject_dialog(sub_name, sub_code):
    st.write(f"Share this code with your students for **{sub_name}**")
    st.code(sub_code, language=None)