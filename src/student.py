import streamlit as st
from Components.header_home import header_dashboard, sub_header_dashboard, custom_text_input
from Components.subject_card import subject_card
from Components.dialog_enroll import enroll_dialog
from Components.footer import footer
from ui.home_screen_bg import dashboard_screen_bg, style_dashboard_layout
from PIL import Image
import numpy as np
import time
from pipeline.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from pipeline.voice_pipeline import get_voice_embedding
from database.db import (
    get_all_students, create_student, check_student_exists,
    get_student_subjects, get_student_attendance, unenroll_student_to_subject,
)


# ─── Main Entry ───────────────────────────────────────────────────
def student_screen():
    style_dashboard_layout()
    dashboard_screen_bg()

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

    sub_header_dashboard("Login using FaceID")
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
            st.warning("Face not found. Make sure your face is clearly visible.")
        elif num_faces > 1:
            st.warning("Multiple faces detected. Please ensure only your face is visible.")
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
                    st.toast(f"Welcome back {student['name']}!", icon="👋")
                    time.sleep(1)
                    st.rerun()
            else:
                st.info("Face not recognized. Please register below.")
                st.session_state.show_registration = True

    # ── Registration Section ──
    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

    if st.session_state.show_registration:
        with st.container(border=True):
            sub_header_dashboard("Register New Profile")

            new_name = custom_text_input(
                "Enter your name",
                "E.g. Vijay Jinjavadiya",
                key="reg_name",
            )
            username = custom_text_input(
                "Enter username",
                "E.g. vijay_74",
                key="reg_username",
            )

            st.subheader("Optional Voice Enrollment")
            st.info("Record a short voice sample to enable voice attendance.")

            audio_data = st.audio_input(
                "Say: 'My name is ... and I am present.'"
            )

            if st.button("Create Account", type="primary", width="stretch"):
                if img is None:
                    st.error("Please capture your face first.")
                    st.stop()

                if not username or not username.strip() or not new_name or not new_name.strip():
                    st.warning("All fields are required!")
                    st.stop()

                if check_student_exists(username.strip()):
                    st.error("Username already taken. Choose a different one.")
                    st.stop()

                with st.spinner("Creating profile..."):
                    encodings = get_face_embeddings(img)

                    if not encodings:
                        st.error("Couldn't extract facial features. Try a clearer photo.")
                        st.stop()

                    face_emb = encodings[0].tolist()

                    voice_emb = None
                    if audio_data is not None:
                        voice_emb = get_voice_embedding(audio_data.read())

                    try:
                        response_data = create_student(
                            name=new_name.strip(),
                            username=username.strip(),
                            face_embedding=face_emb,
                            voice_embedding=voice_emb,
                        )
                    except Exception as e:
                        st.error(f"Registration failed: {str(e)}")
                        st.stop()

                    if response_data:
                        train_classifier()

                        st.session_state.student_data = response_data[0]
                        st.session_state.user_role = "student"
                        st.session_state.show_registration = False

                        st.toast(f"Profile created! Hi {new_name}!", icon="🎉")
                        time.sleep(1)
                        st.rerun()


# ─── Student Dashboard ────────────────────────────────────────────
def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    c1, c2 = st.columns([5, 2], vertical_alignment='center')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {student_data['name']}")
        if st.button(
            "Logout",
            type="primary",
            icon=":material/arrow_back:",
            key='loginbackbtn',
            shortcut="control+backspace",
        ):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

    st.space()

    # ── Header + Enroll Button ──
    hc1, hc2 = st.columns([3, 1])
    with hc1:
        sub_header_dashboard("Your Enrolled Subjects")
    with hc2:
        if st.button("➕ Enroll in Subject", type="primary", width="stretch"):
            enroll_dialog()

    st.divider()

    # ── Load Data ──
    with st.spinner("Loading your subjects..."):
        enrollments = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    if not enrollments:
        st.info("📚 You haven't enrolled in any subjects yet. Click 'Enroll in Subject' above!")
        footer()
        return

    # ── Build Attendance Stats ──
    stats_map = {}
    for log in logs:
        sid = log.get('subject_id')
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1
        if log.get('is_present'):
            stats_map[sid]['attended'] += 1

    # ── Overall Summary ──
    total_classes = sum(s['total'] for s in stats_map.values())
    total_attended = sum(s['attended'] for s in stats_map.values())
    overall_pct = round((total_attended / total_classes * 100), 1) if total_classes > 0 else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Subjects", len(enrollments))
    with m2:
        st.metric("Total Classes", total_classes)
    with m3:
        st.metric("Attended", total_attended)
    with m4:
        st.metric("Attendance %", f"{overall_pct}%")

    st.divider()

    # ── Subject Cards ──
    cols = st.columns(2)
    for i, enrollment in enumerate(enrollments):
        sub = enrollment.get('subjects', {}) or {}
        if not sub:
            continue

        subject_id = sub.get('subject_id', enrollment.get('subject_id'))
        s = stats_map.get(subject_id, {"total": 0, "attended": 0})
        pct = round((s['attended'] / s['total'] * 100), 1) if s['total'] > 0 else 0

        stats = [
            ("📊", "attended", f"{s['attended']}/{s['total']}"),
            ("📈", "percentage", f"{pct}%"),
        ]

        def make_unenroll_btn(sid, sname, subj_id):
            def unenroll_btn():
                if st.button(f"🚪 Unenroll", key=f"unenroll_{subj_id}", type="primary"):
                    try:
                        unenroll_student_to_subject(sid, subj_id)
                        st.toast(f"Unenrolled from {sname}", icon="👋")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            return unenroll_btn

        with cols[i % 2]:
            subject_card(
                name=sub.get('name', '—'),
                code=sub.get('subject_code', '—'),
                section=sub.get('section', '—'),
                stats=stats,
                footer_callback=make_unenroll_btn(
                    student_id,
                    sub.get('name', ''),
                    subject_id,
                ),
            )

    footer()
