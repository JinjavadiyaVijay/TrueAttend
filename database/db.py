from database.config import supabase
import bcrypt
from datetime import datetime


# ─── Password Helpers ─────────────────────────────────────────────
def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


# ─── Teacher CRUD ─────────────────────────────────────────────────
def check_teacher_exists(username):
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"username": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


# ─── Student CRUD ─────────────────────────────────────────────────
def check_student_exists(username):
    response = supabase.table("students").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_student(name, username, face_embedding=None, voice_embedding=None):
    data = {
        'username': username,
        'name': name,
        'face_embedding': face_embedding,
        'voice_embedding': voice_embedding,
    }
    response = supabase.table('students').insert(data).execute()
    return response.data

def get_all_students():
    response = supabase.table('students').select("*").execute()
    return response.data


# ─── Subject CRUD ─────────────────────────────────────────────────
def create_subject(subject_code, name, section, teacher_id):
    data = {
        "subject_code": subject_code,
        "name": name,
        "section": section,
        "teacher_id": teacher_id,
    }
    response = supabase.table("subjects").insert(data).execute()
    return response.data

def get_subject_by_code(code):
    """Look up a subject by its unique code."""
    response = supabase.table("subjects").select("*").eq("subject_code", code).execute()
    if response.data:
        return response.data[0]
    return None

def delete_subject(subject_id):
    """Delete a subject and cascade (Supabase handles FK cascades if configured)."""
    # Remove enrollments first
    supabase.table("subject_students").delete().eq("subject_id", subject_id).execute()
    # Remove attendance logs
    supabase.table("attendance_logs").delete().eq("subject_id", subject_id).execute()
    # Remove subject
    response = supabase.table("subjects").delete().eq("subject_id", subject_id).execute()
    return response.data

def get_teacher_subject(teacher_id):
    """Get all subjects for a teacher with student count and class count."""
    response = (
        supabase.table('subjects')
        .select("*")
        .eq("teacher_id", teacher_id)
        .execute()
    )
    subjects = response.data or []

    for sub in subjects:
        subject_id = sub.get('subject_id')


        try:
            enroll_resp = (
                supabase.table('subject_students')
                .select("student_id", count="exact")
                .eq("subject_id", subject_id)
                .execute()
            )
            sub['total_students'] = enroll_resp.count if enroll_resp.count is not None else len(enroll_resp.data)
        except Exception:
            sub['total_students'] = 0

        try:
            att_resp = (
                supabase.table('attendance_logs')
                .select("timestamp")
                .eq("subject_id", subject_id)
                .execute()
            )
            timestamps = [log['timestamp'] for log in (att_resp.data or [])]
            sub['total_classes'] = len(set(timestamps))
        except Exception:
            sub['total_classes'] = 0

    return subjects


# ─── Subject Enrollment ──────────────────────────────────────
def get_subject_students(subject_id):
    """Get all students enrolled in a subject."""
    response = (
        supabase.table('subject_students')
        .select("*, students(*)")
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data or []

def enroll_student_to_subject(student_id, subject_id):
    """Enroll a student in a subject. Returns None if already enrolled."""
    # Check for duplicate
    existing = (
        supabase.table("subject_students")
        .select("*")
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    if existing.data:
        return None  # Already enrolled

    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(student_id, subject_id):
    response = (
        supabase.table("subject_students")
        .delete()
        .eq("student_id", student_id)
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data

def get_student_subjects(student_id):
    response = (
        supabase.table('subject_students')
        .select("*, subjects(*, teachers(name))")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data or []


# ─── Attendance ───────────────────────────────────────────────────
def create_attendance(subject_id, logs):
    """
    Bulk-insert attendance records.
    logs: list of dicts with keys: student_id, is_present
    """
    timestamp = datetime.now().isoformat()
    records = []
    for log in logs:
        records.append({
            "subject_id": subject_id,
            "student_id": log['student_id'],
            "is_present": log['is_present'],
            "timestamp": timestamp,
        })

    if records:
        response = supabase.table("attendance_logs").insert(records).execute()
        return response.data
    return []

def get_attendance_for_teacher(teacher_id):
    """Get all attendance logs across a teacher's subjects."""
    # First get teacher's subject IDs
    subjects = get_teacher_subject(teacher_id)
    subject_ids = [s['subject_id'] for s in subjects]

    if not subject_ids:
        return []

    response = (
        supabase.table('attendance_logs')
        .select("*, students(name, username), subjects(name, subject_code, section)")
        .in_("subject_id", subject_ids)
        .order("timestamp", desc=True)
        .execute()
    )
    return response.data or []

def get_student_attendance(student_id):
    """Get all attendance records for a specific student."""
    response = (
        supabase.table('attendance_logs')
        .select("*, subjects(name, subject_code)")
        .eq("student_id", student_id)
        .order("timestamp", desc=True)
        .execute()
    )
    return response.data or []
