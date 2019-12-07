from enum import Enum

class Instructor:
    idno = 0
    last_name = ""
    first_name = ""
    middle_name = ""
    
    def __init__(self, idno, last, first, middle):
        self.idno = idno
        self.last_name = last
        self.first_name = first
        self.middle_name = middle
    
    def get_id(self):
        return self.idno

    def get_last(self):
        return self.last_name

    def get_first(self):
        return self.first_name

    def get_middle(self):
        return self.middle_name

class Class:
    cid = 0
    course = None
    section = ""
    term = 0
    instructor = None
    room = None
    classlimit = 0

    def __init__(self, cid, course, section, term, instructor, room, classlimit):
        self.cid = cid
        self.course = course
        self.section = section
        self.term = term
        self.instructor = instructor
        self.room = room
        self.classlimit = classlimit

    def get_id(self):
        return self.cid

    def get_course(self):
        return self.course

    def get_section(self):
        return self.section

    def get_term(self):
        return self.term

    def get_instructor(self):
        return self.instructor

    def get_room(self):
        return self.room

    def get_class_limit(self):
        return self.classlimit

class Room:
    rid = 0
    location = ""

    def __init__(self, rid, location):
        self.rid = rid
        self.location = location

    def get_id(self):
        return self.rid

    def get_location(self):
        return self.location
