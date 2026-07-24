import streamlit as st
from Components.header_home import header_home
from ui.home_screen_bg import home_screen_bg, style_base_layout


def home_screen():
    style_base_layout()
    home_screen_bg()
    header_home()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("I'm Teacher")
        st.image("Assets/Professor-cuate (1).svg")
        if st.button("Teacher", type="primary", icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_state"] = "teacher"
            st.rerun()
    
    with col2:
        st.subheader("I'm Student")
        st.image("Assets/Learning-cuate.svg")
        if st.button("Student", type="primary",icon=':material/arrow_outward:', icon_position='right'):
            st.session_state["login_state"] = "student"
            st.rerun()