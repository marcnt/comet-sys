import sqlite3
from sqlite3 import Error, IntegrityError

from model.user import User, UserType
from model.cclass import Class, Instructor, Room
from model.course import Course

from datetime import date

import os.path

class Database:
    connection = None
    
    def __init__(self, file):
        is_new = True
        if os.path.exists(file):
            is_new = False

        try:
            conn = sqlite3.connect(file)
            if conn is not None:
                self.connection = conn
                if is_new:
                    self.reset()
        except Error as e:
            print(e)

    def run_sql(self, sql):
        try:
            c = self.connection.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def reset(self):
        try:
            cur = self.connection.cursor()
            with open("reset.sql", "r") as file:
                cur.executescript(file.read())
            self.connection.commit()
        except Error as e:
            print(e)
        
        today = date.today()
        idno = today.year * 10000 + 1
        password = "password"
        self.new_admin(idno, password, "", "", "")

        self.new_instructor(0, "", "", "")

        print("An initial admin account has been created. The ID number is " + str(idno) + " and the password is: " + password)

    def new_student(self, idno, password, last, first, middle):
        sql_create_user = """
                          INSERT INTO USERS (idno, type, lastname, firstname, middlename, password)
                          VALUES (?, 'S', ?, ?, ?, ?);
                          """
        sql_create_student = """
                             INSERT INTO STUDENTS (idno)
                             VALUES (?);
                             """

        try:
            cur = self.connection.cursor()
            cur.execute(sql_create_user, (idno, last, first, middle, password));
            cur.execute(sql_create_student, (idno,))
            self.connection.commit()
            return User(idno, UserType.STUDENT, last, first, middle)
        except IntegrityError as e:
            print("A user with the same ID number exists already.")
        except Error as e:
            print(e)
        
        return None

    def new_admin(self, idno, password, last, first, middle):
        sql_create_user = """
                          INSERT INTO USERS (idno, type, lastname, firstname, middlename, password)
                          VALUES (?, 'A', ?, ?, ?, ?);
                          """
        sql_create_admin = """
                           INSERT INTO ADMINS (idno)
                           VALUES (?);
                           """

        try:
            cur = self.connection.cursor()
            cur.execute(sql_create_user, (idno, last, first, middle, password));
            cur.execute(sql_create_admin, (idno,))
            self.connection.commit()
            return User(idno, UserType.ADMIN, last, first, middle)
        except IntegrityError as e:
            print("A user with the same ID number exists already.")
        except Error as e:
            print(e)
        
        return None

    def get_user(self, idno):
        cur = self.connection.cursor()
        cur.execute("SELECT type, lastname, firstname, middlename FROM USERS WHERE idno = ?", (idno,))
        row = cur.fetchone()
        if row is not None:
            if row[0] == 'A':
                # we have an admin
                return User(idno, UserType.ADMIN, row[1], row[2], row[3])
            elif row[0] == 'S':
                # we have a student
                return User(idno, UserType.STUDENT, row[1], row[2], row[3])
            else:
                raise Error("Invalid user type")
        else:
            return None

    def edit_user(self, idno, last, first, middle):
        sql_update_user = "UPDATE USERS SET lastname = ?, firstname = ?, middlename = ? WHERE idno = ?"

        cur = self.connection.cursor()
        cur.execute(sql_update_user, (last, first, middle, idno));
        self.connection.commit()

    def edit_password(self, idno, password):
        sql_update_user = "UPDATE USERS SET password = ? WHERE idno = ?"

        cur = self.connection.cursor()
        cur.execute(sql_update_user, (password, idno));
        self.connection.commit()

    def new_instructor(self, idno, last, first, middle):
        sql_create_instructor = "INSERT INTO INSTRUCTORS (idno, lastname, firstname, middlename) VALUES (?, ?, ?, ?);"
        
        try:
            cur = self.connection.cursor()
            cur.execute(sql_create_instructor, (idno, last, first, middle));
            self.connection.commit()
            return Instructor(idno, last, first, middle)
        except IntegrityError as e:
            print("An instructor with the same ID number exists already.")
        except Error as e:
            print(e)
        
        return None

    def get_instructor(self, idno):
        cur = self.connection.cursor()
        cur.execute("SELECT lastname, firstname, middlename FROM INSTRUCTORS WHERE idno = ?", (idno,))
        row = cur.fetchone()
        if row is not None:
            return Instructor(idno, row[0], row[1], row[2])
        else:
            return None

    def get_instructors(self):
        cur = self.connection.cursor()
        cur.execute("SELECT idno, lastname, firstname, middlename FROM INSTRUCTORS WHERE idno != 0 ORDER BY lastname, firstname, middlename, idno")
        rows = cur.fetchall()
        return map(lambda row : Instructor(row[0], row[1], row[2], row[3]), rows)

    def edit_instructor(self, idno, last, first, middle):
        sql_update_instructor = "UPDATE INSTRUCTORS SET lastname = ?, firstname = ?, middlename = ? WHERE idno = ?"
        
        cur = self.connection.cursor()
        cur.execute(sql_update_instructor, (last, first, middle, idno));
        self.connection.commit()
        return Instructor(idno, last, first, middle)

    def delete_instructor(self, idno):
        if idno == 0:
            return False
            
        cur = self.connection.cursor()
        cur.execute("DELETE FROM INSTRUCTORS WHERE idno = ?", (idno,));
        count = cur.rowcount > 0
        self.connection.commit()
        return count

    def new_room(self, location):
        sql_create_room = "INSERT INTO ROOMS (location) VALUES (?);"
        cur = self.connection.cursor()
        cur.execute(sql_create_room, (location,));
        self.connection.commit()
        return Room(cur.lastrowid, location)

    def get_room(self, location):
        cur = self.connection.cursor()
        cur.execute("SELECT roomid FROM ROOMS WHERE location = ?", (location,))
        row = cur.fetchone()
        if row is not None:
            return Room(row[0], location)
        else:
            return None

    def get_rooms(self):
        cur = self.connection.cursor()
        cur.execute("SELECT roomid, location FROM ROOMS ORDER BY location")
        rows = cur.fetchall()
        return map(lambda row : Room(row[0], row[1]), rows)

    def delete_room(self, location):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM ROOMS WHERE location = ?", (location,));
        count = cur.rowcount > 0
        self.connection.commit()
        return count

    def new_course(self, coursecode, name, units, is_academic):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO COURSES (coursecode, name, units, is_academic) VALUES (?, ?, ?, ?)", (coursecode, name, units, 1 if is_academic else 0))
        self.connection.commit()
        return Course(cur.lastrowid, coursecode, name, units, is_academic, [])

    def get_course(self, coursecode):
        cur = self.connection.cursor()
        cur.execute("SELECT courseid, name, units, is_academic FROM COURSES WHERE coursecode = ?", (coursecode,))
        row = cur.fetchone()
        if row is not None:
            return Course(row[0], coursecode, row[1], row[2], row[3] == 1, [])
        else:
            return None

    def get_courses(self):
        cur = self.connection.cursor()
        cur.execute("SELECT courseid, coursecode, name, units, is_academic FROM COURSES ORDER BY coursecode")
        rows = cur.fetchall()
        return map(lambda row : Course(row[0], row[1], row[2], row[3], row[4], []), rows)
        
    def delete_course(self, coursecode):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM COURSES WHERE coursecode = ?", (coursecode,));
        count = cur.rowcount > 0
        self.connection.commit()
        return count

    def new_prerequisite(self, course, prereq, type):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO PREREQS (courseid, prerequisite, type) VALUES (?, ?, ?)", (course.get_id(), prereq.get_id(), type))
        self.connection.commit()
        return (prereq, type)

    def new_class(self, course : Course, section, term, classlimit):
        sql_create_class = """
                           INSERT INTO CLASSES (courseid, section, term, instructor, classlimit)
                           VALUES (?, ?, ?, ?, ?)
                           """

        cur = self.connection.cursor()
        cur.execute(sql_create_class, (course.get_id(), section, term, 0, classlimit))
        self.connection.commit()
        return Class(cur.lastrowid, course, section, term, None, classlimit, [])

    def get_classes(self, course, term):
        sql_select_class = """
                           SELECT classid, section, idno, lastname, firstname, middlename, classlimit
                           FROM CLASSES
                           JOIN INSTRUCTORS ON instructor = idno
                           WHERE courseid = ? AND term = ?
                           """
        
        cur = self.connection.cursor()
        cur.execute(sql_select_class, (course.get_id(), term))
        rows = cur.fetchall()
        return map(lambda row : Class(row[0], course, row[1], term, None if row[2] == 0 else Instructor(row[2], row[3], row[4], row[5]), row[6], []), rows)

    def delete_class(self, classid):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM CLASSES WHERE classid = ?", (classid,));
        count = cur.rowcount > 0
        self.connection.commit()
        return count

    def assign_instructor(self, classid, instructor):
        cur = self.connection.cursor()
        cur.execute("UPDATE CLASSES SET instructor = ? WHERE classid = ?", (instructor.get_id(), classid))
        self.connection.commit()

    def login(self, idno, password):
        sql_login = """
                    SELECT type, lastname, firstname, middlename
                    FROM USERS
                    WHERE idno = ? AND password = ?;
                    """

        cur = self.connection.cursor()
        cur.execute(sql_login, (idno, password))
        row = cur.fetchone()

        if row is not None:
            if row[0] == 'A':
                # we have an admin
                return User(idno, UserType.ADMIN, row[1], row[2], row[3])
            elif row[0] == 'S':
                # we have a student
                return User(idno, UserType.STUDENT, row[1], row[2], row[3])
            else:
                raise Error("Invalid user type")
        else:
            return None