"""
Student model
"""

from .user import db


class Student(db.Model):
    """Student model"""
    
    __tablename__ = 'student'
    
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), unique=True, nullable=False)
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'), nullable=False)
    division_id = db.Column(db.Integer, db.ForeignKey('division.division_id'), nullable=False)
    enrollment_no = db.Column(db.String(50), unique=True, nullable=False)
    roll_no = db.Column(db.Integer, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('faculty.faculty_id'))
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.semester_id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='student')
    department = db.relationship('Department', back_populates='students')
    division = db.relationship('Division', back_populates='students')
    mentor = db.relationship('Faculty', foreign_keys=[mentor_id], back_populates='students_mentored')
    semester = db.relationship('Semester', back_populates='students')
    attendances = db.relationship('Attendance', back_populates='student', cascade='all, delete-orphan')
    parents = db.relationship('Parent', back_populates='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.enrollment_no} - {self.user.name if self.user else "Unknown"}>'
    
    def verify_enrollment_user_match(self):
        """Verify that enrollment_no is properly matched with user_id"""
        if not self.user:
            return False, "User not found for this student"
        if not self.enrollment_no:
            return False, "Enrollment number not set"
        return True, "Valid"
    
    def get_attendance_percentage(self, semester_id=None):
        """Calculate attendance percentage for a semester"""
        from models.attendance import Attendance
        from models.lecture import Lecture
        from models.timetable import Timetable
        from models.subject import Subject
        
        query = Attendance.query.filter_by(student_id=self.student_id)
        
        if semester_id:
            # Filter by semester if provided
            query = query.join(Lecture).join(Timetable).join(Subject).filter(
                Subject.semester_id == semester_id
            )
        
        total_lectures = query.count()
        if total_lectures == 0:
            return 0.0
        
        present_count = query.filter(
            Attendance.status_id == 1  # PRESENT status
        ).count()
        
        return (present_count / total_lectures) * 100 if total_lectures > 0 else 0.0
    
    @staticmethod
    def get_by_enrollment_no(enrollment_no):
        """Get student by enrollment number with validation"""
        student = Student.query.filter_by(enrollment_no=enrollment_no).first()
        if student:
            is_valid, msg = student.verify_enrollment_user_match()
            if is_valid:
                return student
        return None
    
    @staticmethod
    def get_by_user_id(user_id):
        """Get student by user_id"""
        return Student.query.filter_by(user_id=user_id).first()

