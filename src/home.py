import streamlit as st
from Components.header_home import header_home
from ui.home_screen_bg import home_screen_bg, style_base_layout


def home_screen():
    style_base_layout()
    home_screen_bg()
    header_home()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Teacher"):
            st.session_state["login_state"] = "teacher"
            st.rerun()
    with col2:
        if st.button("student"):
            st.session_state["login_state"] = "student"
            st.rerun()
