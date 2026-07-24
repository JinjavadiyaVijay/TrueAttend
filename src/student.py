import streamlit as st
from Components.header_home import header_dashboard
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout


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
