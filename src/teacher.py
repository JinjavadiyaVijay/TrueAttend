import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
from functools import partial
from datetime import datetime

from Components.header_home import header_dashboard, sub_header_dashboard, custom_text_input
from Components.dialog import create_subject_dailog, share_subject_dialog
from Components.subject_card import subject_card
from Components.dialog_attendance_results import attendance_result_dialog
from Components.footer import footer
from ui.home_screen_bg import dashboard_screen_bg, style_dashboard_layout
from database.db import (
    check_teacher_exists, create_teacher, teacher_login,
    create_subject, get_teacher_subject, delete_subject,
    get_subject_students, get_attendance_for_teacher,
)
from pipeline.face_pipeline import predict_attendance, get_face_embeddings
from pipeline.voice_pipeline import process_bulk_audio


# ─── Main Entry ───────────────────────────────────────────────────
def teacher_screen():
    style_dashboard_layout()
    dashboard_screen_bg()

    if "teacher_login_type" not in st.session_state:
        st.session_state.teacher_login_type = "login"

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state.teacher_login_type == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()


# ─── Dashboard ────────────────────────────────────────────────────
def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns([5, 2], vertical_alignment='center')

    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button(
            "Log out",
            type="primary",
            icon=":material/arrow_back:",
            icon_position="left",
            shortcut="control+backspace",
            key='longinbackbtn',
        ):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendence'

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "secondary" if st.session_state.current_teacher_tab == 'take_attendence' else 'tertiary'
        if st.button('Take Attendence', width='stretch', type=type1, icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendence'
            st.rerun()

    with tab2:
        type2 = "secondary" if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button('Manage Subject', width='stretch', type=type2, icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "secondary" if st.session_state.current_teacher_tab == 'attendence_records' else 'tertiary'
        if st.button('Attendence Record', width='stretch', type=type3, icon=':material/assignment:'):
            st.session_state.current_teacher_tab = 'attendence_records'
            st.rerun()

    st.markdown("""
        <hr style="
            border: none;
            height: 1px;
            background: rgba(0, 0, 0, 0.18);
            margin: 24px 0;
        ">
        """, unsafe_allow_html=True)

    if st.session_state.current_teacher_tab == 'take_attendence':
        teacher_tab_take_attendence()
    if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attendence_records':
        teacher_tab_attendence_records()

    footer()


# ─── Take Attendance Tab ─────────────────────────────────────────
def teacher_tab_take_attendence():
    sub_header_dashboard('Take AI Attendance')

    teacher_id = st.session_state.teacher_data['teacher_id']
    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.info("📚 No subjects found. Create a subject first in 'Manage Subjects'.")
        return

    subject_names = [s['name'] for s in subjects]
    selected_name = st.selectbox("Select Subject", subject_names, index=0)
    selected_subject = next(s for s in subjects if s['name'] == selected_name)
    subject_id = selected_subject['subject_id']

    # Get enrolled students for this subject
    enrolled = get_subject_students(subject_id)
    enrolled_student_ids = [e['student_id'] for e in enrolled]

    if not enrolled_student_ids:
        st.warning("⚠️ No students enrolled in this subject yet. Share the subject code with students.")
        return

    st.markdown(f"**{len(enrolled_student_ids)}** students enrolled in **{selected_name}**")

    st.divider()

    # ── Photo Attendance ──
    st.markdown(
        "<h4 style='color:#ff9800;'>📷 Upload class photo or use camera</h4>",
        unsafe_allow_html=True,
    )

    input_method = st.radio(
        "Input method",
        ["Camera", "Upload Photo"],
        horizontal=True,
        label_visibility="collapsed",
    )

    class_image = None
    if input_method == "Camera":
        photo = st.camera_input("Capture class photo", label_visibility="collapsed")
        if photo:
            class_image = np.array(Image.open(photo))
    else:
        uploaded = st.file_uploader("Upload class photo", type=["jpg", "jpeg", "png"])
        if uploaded:
            class_image = np.array(Image.open(uploaded))
            st.image(class_image, caption="Uploaded photo", use_container_width=True)

    if class_image is not None:
        if st.button("🔍 Run Face Attendance", type="primary", width="stretch"):
            with st.spinner("AI is scanning faces..."):
                detected, all_ids, num_faces = predict_attendance(class_image)

            st.toast(f"Detected {num_faces} face(s)", icon="🔍")

            if num_faces == 0:
                st.warning("No faces detected in the photo. Try again with a clearer image.")
                return

            # Build attendance logs
            from database.db import get_all_students
            all_students = get_all_students()
            student_map = {s['student_id']: s['name'] for s in all_students}

            logs = []
            rows = []
            for sid in enrolled_student_ids:
                is_present = sid in detected
                logs.append({"student_id": sid, "is_present": is_present})
                rows.append({
                    "Name": student_map.get(sid, f"ID {sid}"),
                    "Status": "✅ Present" if is_present else "❌ Absent",
                })

            df = pd.DataFrame(rows)
            attendance_result_dialog(subject_id, selected_name, df, logs)

    st.divider()

    # ── Voice Attendance ──
    st.markdown(
        "<h4 style='color:#ff9800;'>🎤 Voice Attendance (Optional)</h4>",
        unsafe_allow_html=True,
    )
    st.info("Record classroom audio. The AI will identify students by voice.")

    audio_data = st.audio_input("Record classroom audio")

    if audio_data and st.button("🔊 Run Voice Attendance", type="primary", width="stretch"):
        with st.spinner("Analyzing voices..."):
            from database.db import get_all_students
            all_students = get_all_students()
            student_map = {s['student_id']: s['name'] for s in all_students}

            # Build candidates dict: {student_id: voice_embedding}
            candidates = {}
            for sid in enrolled_student_ids:
                student = next((s for s in all_students if s['student_id'] == sid), None)
                if student and student.get('voice_embedding'):
                    candidates[sid] = student['voice_embedding']

            if not candidates:
                st.warning("No enrolled students have voice profiles. Voice attendance requires students to register with voice.")
                return

            results = process_bulk_audio(audio_data.read(), candidates)

        logs = []
        rows = []
        for sid in enrolled_student_ids:
            is_present = sid in results
            logs.append({"student_id": sid, "is_present": is_present})
            rows.append({
                "Name": student_map.get(sid, f"ID {sid}"),
                "Status": "✅ Present" if is_present else "❌ Absent",
                "Confidence": f"{results.get(sid, 0):.2f}" if sid in results else "—",
            })

        df = pd.DataFrame(rows)
        attendance_result_dialog(subject_id, selected_name, df, logs)


# ─── Manage Subjects Tab ─────────────────────────────────────────
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1,_,col2 = st.columns([1,2,1],gap='large')
    with col1:
        st.markdown(
        f"""
            <h3 style="margin:0;padding:0;font:800 1.5rem 'Sora',sans-serif;color:#063B00;line-height:1.2;">
            Manage Subjects
            </h3>
        """,
        unsafe_allow_html=True,
        )
    with col2:
        if st.button("Create New Subject", type="primary",width='stretch'):
            create_subject_dailog(teacher_id)

    # List all subjects
    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.info("📚 No subjects yet. Click 'Create New Subject' to get started!")
        return

    for sub in subjects:
        stats = [
            ("👥", "students", sub['total_students']),
            ("🕰️", "classes", sub['total_classes']),
        ]

        # Use partial to avoid closure bug — captures current sub values
        def make_share_btn(name, code):
            def share_btn():
                sc1, sc2,_,_,_,_= st.columns(6)
                with sc1:
                    if st.button(f"📤 Share Code", key=f"share_{code}", type="primary"):
                        share_subject_dialog(name, code)
                with sc2:
                    if st.button(f"🗑️ Delete", key=f"del_{code}"):
                        try:
                            delete_subject(sub['subject_id'])
                            st.toast(f"Deleted {name}", icon="🗑️")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            return share_btn

        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=make_share_btn(sub['name'], sub['subject_code']),
        )


# ─── Attendance Records Tab ──────────────────────────────────────
def teacher_tab_attendence_records():
    sub_header_dashboard('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    with st.spinner("Loading records..."):
        logs = get_attendance_for_teacher(teacher_id)

    if not logs:
        st.info("📋 No attendance records yet. Take attendance to see records here.")
        return

    # Build DataFrame
    rows = []
    for log in logs:
        student_info = log.get('students', {}) or {}
        subject_info = log.get('subjects', {}) or {}
        rows.append({
            "Date": log.get('timestamp', '')[:10] if log.get('timestamp') else '',
            "Time": log.get('timestamp', '')[11:16] if log.get('timestamp') else '',
            "Subject": subject_info.get('name', '—'),
            "Code": subject_info.get('subject_code', '—'),
            "Section": subject_info.get('section', '—'),
            "Student": student_info.get('name', '—'),
            "Username": student_info.get('username', '—'),
            "Status": "✅ Present" if log.get('is_present') else "❌ Absent",
        })

    df = pd.DataFrame(rows)

    # Filters
    fc1, fc2 = st.columns(2)
    with fc1:
        subject_options = ["All"] + sorted(df['Subject'].unique().tolist())
        selected_subject = st.selectbox("Filter by Subject", subject_options)
    with fc2:
        date_options = ["All"] + sorted(df['Date'].unique().tolist(), reverse=True)
        selected_date = st.selectbox("Filter by Date", date_options)

    filtered = df.copy()
    if selected_subject != "All":
        filtered = filtered[filtered['Subject'] == selected_subject]
    if selected_date != "All":
        filtered = filtered[filtered['Date'] == selected_date]

    # Summary metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Records", len(filtered))
    with m2:
        present_count = len(filtered[filtered['Status'] == "✅ Present"])
        st.metric("Present", present_count)
    with m3:
        absent_count = len(filtered[filtered['Status'] == "❌ Absent"])
        st.metric("Absent", absent_count)

    st.divider()

    # Data table
    st.dataframe(filtered, hide_index=True, use_container_width=True)

    # CSV Export
    st.divider()
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export as CSV",
        data=csv,
        file_name=f"attendance_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
        type="primary",
    )


# ─── Auth Logic ───────────────────────────────────────────────────
def register_teacher(teacher_name, teacher_username, teacher_password, teacher_password_confirm):
    if not teacher_name or not teacher_password or not teacher_password_confirm or not teacher_username:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_password != teacher_password_confirm:
        return False, "Password doesn't match"
    if len(teacher_password) < 6:
        return False, "Password must be at least 6 characters"

    try:
        create_teacher(teacher_username, teacher_password, teacher_name)
        return True, "Successfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


# ─── Login Screen ─────────────────────────────────────────────────
def teacher_screen_login():
    c1, c2 = st.columns([5, 2], vertical_alignment='center')

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

    sub_header_dashboard("Login using password")
    st.space()
    teacher_username = st.text_input("Enter username", placeholder='Enter your username')

    teacher_password = st.text_input("Enter your password", type="password", placeholder='Enter Password')

    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_password):
                st.toast("Welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password")
    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()


# ─── Register Screen ─────────────────────────────────────────────
def teacher_screen_register():
    c1, c2 = st.columns([5, 2], vertical_alignment='center')

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

    sub_header_dashboard("Register your profile Here")
    st.space()
    teacher_name = st.text_input("Enter name", placeholder='Enter your full name')

    teacher_username = st.text_input("Enter username", placeholder='Choose a username')

    teacher_password = st.text_input("Enter your password", type='password', placeholder='Enter Password')

    teacher_password_confirm = st.text_input("Confirm your password", type='password', placeholder='Confirm Password')

    st.markdown("""
        <hr style="
            border: none;
            border-top: 3px solid red;
            margin: 20px 0;
        ">
        """, unsafe_allow_html=True)

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button('Register Now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_name, teacher_username, teacher_password, teacher_password_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)
    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()
