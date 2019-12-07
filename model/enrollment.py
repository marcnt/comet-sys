from enum import Enum

class EnrollStatus(Enum):
    ENROLLED        = 1
    DROPPED         = 2

class Enrollment:
    eid = 0
    student = None
    cclass = None
    status = None

    def __init__(self, eid, student, cclass, status):
        self.eid = eid
        self.student = student
        self.cclass = cclass
        self.status = status

    def get_id(self):
        return self.eid

    def get_student(self):
        return self.student

    def get_class(self):
        return self.cclass

    def get_status(self):
        return self.status
