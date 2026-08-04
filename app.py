import streamlit as st
from src.home import home_screen
from src.teacher import teacher_screen
from Components.dialog_enroll import auto_enroll_dialog
from src.student import student_screen

st.set_page_config(
    page_title="TrueAttend — AI Attendance System",
    page_icon="🎓",
    layout="wide",
)

JOIN_QUERY_PARAM = "join_code"
PENDING_JOIN_CODE_KEY = "pending_join_code"


def _get_query_join_code():
    join_code = st.query_params.get(JOIN_QUERY_PARAM)
    if isinstance(join_code, list):
        join_code = join_code[0] if join_code else None
    return join_code.strip() if join_code else None


def _sync_join_code_from_url():
    join_code = _get_query_join_code()
    if join_code:
        st.session_state[PENDING_JOIN_CODE_KEY] = join_code
        return join_code
    return st.session_state.get(PENDING_JOIN_CODE_KEY)


def main():
    if 'login_state' not in st.session_state:
        st.session_state['login_state'] = None

    join_code = _sync_join_code_from_url()
    student_logged_in = (
        "student_data" in st.session_state
        and st.session_state.get("user_role") == "student"
    )

    if join_code and not student_logged_in and st.session_state['login_state'] != 'student':
        st.session_state['login_state'] = 'student'
        st.rerun()

    match st.session_state['login_state']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()

    if join_code and student_logged_in:
        auto_enroll_dialog(join_code)
    
main()
