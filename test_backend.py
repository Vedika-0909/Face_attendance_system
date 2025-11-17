from students import add_student, view_students
from attendance import mark_attendance, fetch_attendance

# Add student
student_id = add_student(
    "102", "Rani Test", "CS", "A", "3rd", "2003-05-17", "Female", "rani.test@gmail.com", "9876543210"
)
print("Student added with ID:", student_id)

# View students
print(view_students())

# Mark attendance
mark_attendance(student_id)
print(fetch_attendance(student_id))
