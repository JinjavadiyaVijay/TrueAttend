import streamlit as st
from Components.header_home import header_dashboard,sub_header_deshboard,custom_text_input
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout
from database.db import check_teacher_exists,create_teacher,teacher_login,create_subject,get_teacher_subject


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
    c1,c2 = st.columns([5,2],vertical_alignment='center',)
    
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Log out",
            type="primary",
            icon=":material/arrow_back:",
            icon_position="left",
            shortcut="control+backspace",
            key='longinbackbtn',
        ):
            st.session_state["is_logged_in"] =False
            del st.session_state.teacher_data 
            st.rerun()
            
    st.space()
    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab='take_attendence'
        
    
    tab1, tab2, tab3 = st.columns(3)
    
    with tab1:
        type1 = "secondary" if st.session_state.current_teacher_tab == 'take_attendence' else 'tertiary'
        if st.button('Take Attendence', width='stretch',type=type1, icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab='take_attendence'       
            st.rerun()
            
    with tab2:
        type2="secondary" if st.session_state.current_teacher_tab=='manage_subjects' else 'tertiary'
        if st.button('Manage Subject', width='stretch',type=type2 ,icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab='manage_subjects'       
            st.rerun()
    
    with tab3:
        type3="secondary" if st.session_state.current_teacher_tab=='attendence_records' else 'tertiary'
        if st.button('Attendence Record', width='stretch', type=type3, icon=':material/assignment:'):
            st.session_state.current_teacher_tab='attendence_records'       
            st.rerun()
    
    st.markdown("""
        <hr style="
            border: none;
            height: 1px;
            background: rgba(0, 0, 0, 0.18);
            margin: 24px 0;
        ">
        """, unsafe_allow_html=True)
       
    if st.session_state.current_teacher_tab=='take_attendence':
        teacher_tab_take_attendence()
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=='attendence_records':
        teacher_tab_attendence_records()

def teacher_tab_take_attendence():
    sub_header_deshboard('Take AI Attendance')

def teacher_tab_manage_subjects():
    sub_header_deshboard('Manage Subject')
    
    teacher_id = st.session_state.teacher_data['teacher_id']
    
    col1,col2 = st.columns(2)
    with col1:
        sub_header_deshboard("Manage Subjects",width= 'stretch') 
    with col2 : 
        if st.button("Create New subject",width='stretch'):
            create_subject-dialog(teacher_id)   
    
    # list all subject
    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats =[
                ("👥","students", sub['total_stundents']),
                ("🕰️","classes", sub['total_classes'])
            ]
        def share_btn():
            if st.button(f"Share Code:{sub['name']}", key=f"share_{sub[subjec_code]}",icon=":material/share:"):
                share_subject_dialog(sub['name'], sub['subject-code'])
            st.space()
            
        subject_card(
            name= sub['name'],
            code = sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else :
        st.info("NO SUBJECT FOUND, CREATE ONE ABOVE")
def teacher_tab_attendence_records():
    sub_header_deshboard('Attendence Record')
    
            
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