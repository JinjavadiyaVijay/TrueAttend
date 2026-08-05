import streamlit as st
from database.db import create_subject

import segno 
import io 
import os
from urllib.parse import urlencode


APP_BASE_URL = os.getenv("TRUEATTEND_BASE_URL", "https://trueattend.streamlit.app")


def _build_join_url(subject_code):
    query = urlencode({"join_code": subject_code})
    return f"{APP_BASE_URL.rstrip('/')}/?{query}"

@st.dialog("Create New Subject")
def create_subject_dailog(teacher_id):
    st.write('Enter the details of new subject')
    st.markdown('<p style="color:white; margin-bottom:0;">Subject Code</p>', unsafe_allow_html=True)
    sub_id = st.text_input("Subject Code", placeholder="C5101", label_visibility="collapsed")
    st.markdown('<p style="color:white; margin-bottom:0;">Subject Name</p>', unsafe_allow_html=True)
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science", label_visibility="collapsed")
    st.markdown('<p style="color:white; margin-bottom:0;">Section</p>', unsafe_allow_html=True)
    sub_section = st.text_input("Section", placeholder="A", label_visibility="collapsed")
    
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
    join_url = _build_join_url(sub_code)

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind='png',scale=10,border=1)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language='text')
        st.code(sub_code, language='text')
        st.info('Copy this link or QR code to invite students to join this subject.')
    
    with col2:
        st.markdown('### Scan QR Code')
        st.image(out.getvalue(),caption='QR Code', width=180)
        st.success(f'Subject: {sub_name}')
