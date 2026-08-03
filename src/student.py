import streamlit as st
from Components.header_home import header_dashboard,sub_header_deshboard,custom_text_input
from ui.home_screen_bg import deshboard_screen_bg, style_dashboard_layout
from PIL import Image
import numpy as np 
import time
from pipeline.face_pipeline import predict_attendance, get_face_embeddings,train_classifier
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

    # Persistent registration state
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    left, right = st.columns([5, 2], gap="medium", vertical_alignment="center")

    with left:
        header_dashboard()

    with right:
        if st.button(
            "Go Back to Home",
            type="primary",
            icon=":material/arrow_back:",
        ):
            st.session_state.login_state = None
            st.session_state.show_registration = False
            st.rerun()

    sub_header_deshboard("Login using FaceID")
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        "<h4 style='color:#ff9800;'>📷 Position your face in the center</h4>",
        unsafe_allow_html=True,
    )

    photo_source = st.camera_input(
        label="camera",
        label_visibility="collapsed",
    )

    img = None

    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):

            detected, all_ids, num_faces = predict_attendance(img)

        if num_faces == 0:
            st.warning("Face not found.")

        elif num_faces > 1:
            st.warning("Multiple faces detected.")

        else:

            if detected:

                student_id = next(iter(detected))

                all_students = get_all_students()

                student = next(
                    (s for s in all_students if s["student_id"] == student_id),
                    None,
                )

                if student:
                    st.session_state.student_data = student
                    st.session_state.user_role = "student"

                    st.toast(f"Welcome back {student['name']}!")

                    time.sleep(1)
                    st.rerun()

            else:
                st.info("Face not recognized. Please register.")
                st.session_state.show_registration = True

    # ---------------- Registration ---------------- #
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

    if st.session_state.show_registration:

        with st.container(border=True):

            sub_header_deshboard("Register New Profile")

            new_name = custom_text_input(
                "Enter your name",
                "E.g. Salmon Bhoiii"
            )
            username=custom_text_input("Enter username","E.g. salmonbhoiii74")
            
            st.subheader("Optional Voice Enrollment")

            st.info(
                "Record a short voice sample to enable voice attendance."
            )

            audio_data = st.audio_input(
                "Say: 'My name is ... and I am present.'"
            )

            if st.button("Create Account", type="primary"):

                if img is None:
                    st.error("Please capture your face first.")
                    st.stop()

                if not username or not new_name.strip():
                    st.warning("All Fields are required!")
                    st.stop()

                with st.spinner("Creating profile..."):

                    encodings = get_face_embeddings(img)

                    if not encodings:
                        st.error(
                            "Couldn't extract facial features."
                        )
                        st.stop()

                    face_emb = encodings[0].tolist()

                    voice_emb = None

                    if audio_data is not None:
                        voice_emb = get_voice_embedding(
                            audio_data.read()
                        )

                    response_data = create_student(
                        name=new_name,
                        username=username,
                        face_embedding=face_emb,
                        voice_embedding=voice_emb,
                    )

                    if response_data:

                        train_classifier()

                        st.session_state.student_data = response_data[0]
                        st.session_state.user_role = "student"
                        st.session_state.show_registration = False

                        st.toast(f"Profile created! Hi {new_name}!")

                        time.sleep(1)
                        st.rerun()
        