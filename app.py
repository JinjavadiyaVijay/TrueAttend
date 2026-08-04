import streamlit as st
from src.home import home_screen
from src.teacher import teacher_screen
from src.student import student_screen

st.set_page_config(
    page_title="TrueAttend — AI Attendance System",
    page_icon="🎓",
    layout="wide",
)

def main():
    if 'login_state' not in st.session_state:
        st.session_state['login_state'] = None

    match st.session_state['login_state']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

main()
