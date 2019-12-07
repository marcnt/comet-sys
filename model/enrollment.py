from enum import Enum

class EnrollStatus(Enum):
    ENROLLED        = 1
    DROPPED         = 2
    # WAITLIST        = 3 NOT IMPLEMENTED

class Enrollment:
    student = None
    cclass = None
    status = None
    enroll_date = None
    grade = 0.0

    def __init__(self, student, cclass, status, enroll_date, grade):
        self.student = student
        self.cclass = cclass
        self.status = status
        self.enroll_date = enroll_date
        self.grade = grade

    def get_student(self):
        return self.student

    def get_class(self):
        return self.cclass

    def get_status(self):
        return self.status

    def get_enroll_date(self):
        return self.enroll_date

    def get_grade(self):
        return self.grade
