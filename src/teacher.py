import streamlit as st
from Components.header_home import header_dashboard,sub_header_deshboard
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout
from database.db import check_teacher_exists,create_teacher,teacher_login


def teacher_screen():
    
    style_dashboard_layout()
    deshboard_screen_bg()
    
    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"
        
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()
        

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f""" Welcome{teacher_data['name']}""")
        
        
def register_teacher (teacher_name,teacher_username,teacher_password,teacher_password_confirm):
    
    if not teacher_name or not teacher_password or not teacher_password_confirm or not teacher_username:
        return False,"All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False,"username already taken "
    if teacher_password != teacher_password_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username,teacher_password,teacher_name)
        return True, "Sucessfuly Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"

def login_teacher(username,password):
    
    if not username or not password :
        return False
    
    teacher = teacher_login(username,password)
    
    if teacher :
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in = True
        return True
    return False
    
    
def teacher_screen_login():
    c1,c2 = st.columns([5,2],vertical_alignment='center',)
    
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Go back to Home",
            type="primary",
            icon=":material/arrow_back:",
            icon_position="left",
            key='longinbackbtn',
        ):
            st.session_state["login_state"] = None
            st.rerun()
            
    sub_header_deshboard("Login using password")
    st.space()
    teacher_username = st.text_input("Enter username",placeholder='salmon bhaiii')
    
    teacher_password = st.text_input("Enter your password",type="password",placeholder = 'Enter Password')
     
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)
    
    btnc1,btnc2 = st.columns(2)
  
    with btnc1:
        if st.button('Login',icon=':material/passkey:',shortcut='control+enter',width = 'stretch') :
            if login_teacher(teacher_username,teacher_password):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")
    with btnc2:
        if st.button('Ragister Insted',type ="primary" ,icon=':material/passkey:',width = 'stretch'):
            st.session_state.teacher_login_type ='register'
            st.rerun()
                     
            
def teacher_screen_register():
    c1,c2 = st.columns([5,2],vertical_alignment='center',)
    
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Go back to Home",
            type="primary",
            icon=":material/arrow_back:",
            icon_position="left",
            key='longinbackbtn'
        ):
            st.session_state["login_state"] = None
            st.rerun()
            
    sub_header_deshboard("Register your profile Here")
    st.space()
    teacher_name = st.text_input("Enter name",placeholder= 'salmonbhaii op')  
    
    teacher_username = st.text_input("Enter username",placeholder='salmon bhaiii')
    
    teacher_password = st.text_input("Enter your password", type='password', placeholder = 'Enter Password')
    
    teacher_password_confirm = st.text_input("confirm your password ", type='password', placeholder = 'Enter Password')
  
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)
    
    btnc1,btnc2 = st.columns(2)
    with btnc1:
        if st.button('Register Now',icon=':material/passkey:',shortcut='control+enter',width = 'stretch'):
            success, message = register_teacher(teacher_name,teacher_username,teacher_password,teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type ="login"
                st.rerun()
            else : 
                st.error(message)
    with btnc2:
        if st.button('Login Insted',type ="primary" ,icon=':material/passkey:',width = 'stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()