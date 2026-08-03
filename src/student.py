import streamlit as st
from Components.header_home import header_dashboard,sub_header_deshboard
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout
from PIL import Image
import numpy as np 
from pipeline.face_pipeline import predict_attendance, get_face_emebeddings,get_trained_model
from pipeline.voice_pipeline import get_voice_embedding
from database.db import get_all_students, create_student

def student_dashboard():
    st.header('Dashboard header')

def student_screen():
    
    style_dashboard_layout()
    deshboard_screen_bg()
    
    if "student_data" in st.session_state:
        student_dashboard()
        return
    
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
    st.space()
    show_registration = False 
    
    photo_source = st.camera_input("position your face in the center ")
    if photo_source:
        img = np.array(Image.open(photo_source))
        
        with st.spinner('AI is scanning..'):
            detected, all_ids, num_faces = predict_attendance(img)
            
            if num_faces == 0:
                st.warning('Face not Found!')
            elif num_faces >1:
                st.warning('Multiple faces Found')
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students  if s['student_id']==student_id),None)
                    
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! you might be a new student!')
                    show_registration = True
    if show_registration:
       with st.container(border=True):
           sub_header_deshboard('Register new Profilr')
           new_name = st.text_input("Enter your name", placeholder="E.g Salmon Bhoiii")
           
           st.subheader('Optional : Voice Enrollment')
           st.info("Enroll Your voice for only attendance")
           
           audio_data = None
           try:
               audio_data = st.audio_input('Record a short phrase like i am present, My name is salmon bhoii.')
           except Exception:
               st.error('Audio Data failed!')
           
           if st.button('Create Account :',type='promary'):
                if new_name:
                    with st.spinner('Create profile..'):
                        img = np.array(Image.open(photo_source))
                        encodings=get_face_emebeddings(img)
                        if encodings:
                            face_emb= encodings[0].tolist()
                            
                            voice_emb = None
                            if audio_data :
                                voice_emb = get_voice_embedding(audio_data.rea())
                                
                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)
                                
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your facial features for registration")
                else:
                    st.warning('Please enter your name!')
                    
           
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)
        