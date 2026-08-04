import streamlit as st
from database.db import create_subject

import segno 
import io 

@st.dialog("Create New Subject")
def create_subject_dailog(teacher_id):
    st.write('Enter the details of new subjecr')
    sub_id = st.text_input("Subject Code",placeholder="C5101")
    sub_name = st.text_input("Subject Name",placeholder="Introduction to Computer Science")
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
    app_domain="http://localhost:8501/"
    join_url=f"{app_domain}/?subject_code={sub_code}"

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind='png',scale=10,border=1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language='text')
        st.code(sub_code, language='text')
        st.info('Copy this link and share and share to students to join class')
    
    with col2:
        st.markdown('### Scan QR Code')
        st.image(out.getvalue(),caption='QR Code', width=180)
        st.success(f'Subject: {sub_name}')


    # st.write(f"Share this code with your students for **{sub_name}**")
    # st.code(sub_code, language=None)
