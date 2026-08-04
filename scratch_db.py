from database.db import get_all_students
students = get_all_students()
if students:
    print(f"Keys: {list(students[0].keys())}")
    print(f"student_id: {students[0].get('student_id')}")
    print(f"id: {students[0].get('id')}")
else:
    print("No students found.")

