import streamlit as st
from Components.header_home import header_dashboard,sub_header_deshboard
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout
from PIL import Image
import numpy as np 


def student_screen():
    style_dashboard_layout()
    deshboard_screen_bg()
    left, right = st.columns([5, 2], gap="medium", vertical_alignment="center")
    with left:
        header_dashboard()
    with right:
        if st.button(
            "Go Back to Home",
            type="primary",
            icon=":material/arrow_back:",
            icon_position="left",
        ):
            st.session_state["login_state"] = None
            st.rerun()
        
    st.space()
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True
        )
    sub_header_deshboard('Login using FaceID',)
    
    photo_source = st.camera_input("position your face in the center ")
    if photo_source:
        np.array(Image.open(photo_source))
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)
        