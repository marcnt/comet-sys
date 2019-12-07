from enum import Enum

class Course:
    course_id = 0
    course_code = ""
    name = ""
    units = 0
    academic = False

    def __init__(self, cid, course_code, name, units, academic):
        self.course_id = cid
        self.course_code = course_code
        self.name = name
        self.units = units
        self.academic = academic

    def get_id(self):
        return self.course_id

    def get_course_code(self):
        return self.course_code

    def get_name(self):
        return self.name

    def get_units(self):
        return self.units

    def is_academic(self):
        return self.academic
