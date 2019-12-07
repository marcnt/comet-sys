from enum import Enum

class UserType(Enum):
    ADMIN   = 1
    STUDENT = 2

class User:
    idno = 0
    type = 0
    last_name = ""
    first_name = ""
    middle_name = ""
    
    def __init__(self, id, type, last, first, middle):
        self.idno = id
        self.type = type
        self.last_name = last
        self.first_name = first
        self.middle_name = middle
    
    def get_id(self):
        return self.idno

    def get_type(self):
        return self.type
    
    def get_last(self):
        return self.last_name

    def get_first(self):
        return self.first_name

    def get_middle(self):
        return self.middle_name
