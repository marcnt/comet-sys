import sqlite3
from sqlite3 import Error

class Database:
    connection = None
    
    def __init__(self, file):
        try:
            conn = sqlite3.connect(file)
            if conn is not None:
                self.connection = conn
                self.create_tables()
        except Error as e:
            print(e)

    def create_tables(self):
        # create the users table
        sql_create_users_table = """CREATE TABLE IF NOT EXISTS USERS (
                                        userid integer PRIMARY KEY,
                                        idno integer NOT NULL,
                                        lastname text NOT NULL,
                                        firstname text NOT NULL,
                                        middlename text NOT NULL,
                                        type integer NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL
                                    );"""
        self.run_sql(sql_create_users_table)
        sql_create_users_index = """CREATE UNIQUE INDEX idx_users_idno ON USERS (idno);"""
        self.run_sql(sql_create_users_index)
        
        sql_create_students_table = """CREATE TABLE IF NOT EXISTS STUDENTS (
                                        studentid integer PRIMARY KEY,
                                        FOREIGN KEY (studentid) REFERENCES USERS (userid)
                                    );"""
        self.run_sql(sql_create_students_table)
        
        sql_create_admins_table = """CREATE TABLE IF NOT EXISTS ADMINS (
                                        userid integer PRIMARY KEY,
                                        FOREIGN KEY (userid) REFERENCES USERS (userid)
                                    );"""
        self.run_sql(sql_create_admins_table)
        
        sql_create_courses_table = """CREATE TABLE IF NOT EXISTS COURSES (
                                        courseid integer PRIMARY KEY,
                                        coursecode text NOT NULL,
                                        name text NOT NULL,
                                        units integer NOT NULL,
                                        is_academic integer NOT NULL
                                    );"""
        self.run_sql(sql_create_courses_table)
        
        sql_create_prereqs_table = """CREATE TABLE IF NOT EXISTS PREREQS (
                                        courseid integer PRIMARY KEY,
                                        prerequisite integer NOT NULL,
                                        type integer NOT NULL,
                                        FOREIGN KEY (courseid) REFERENCES COURSES (courseid),
                                        FOREIGN KEY (prerequisite) REFERENCES COURSES (courseid)
                                    );"""
        self.run_sql(sql_create_prereqs_table)
        
        sql_create_instructors_table = """CREATE TABLE IF NOT EXISTS INSTRUCTORS (
                                            instructorid integer PRIMARY KEY,
                                            lastname text NOT NULL,
                                            firstname text NOT NULL,
                                            middlename text NOT NULL
                                        );"""
        self.run_sql(sql_create_instructors_table)

        sql_create_classes_table = """CREATE TABLE IF NOT EXISTS CLASSES (
                                        classid integer PRIMARY KEY,
                                        courseid integer NOT NULL,
                                        section text NOT NULL,
                                        term integer NOT NULL,
                                        instructor integer NOT NULL,
                                        classlimit integer NOT NULL,
                                        FOREIGN KEY (courseid) REFERENCES COURSES (courseid),
                                        FOREIGN KEY (instructor) REFERENCES INSTRUCTORS (instructorid)
                                    );"""
        self.run_sql(sql_create_classes_table)

        sql_create_rooms_table = """CREATE TABLE IF NOT EXISTS ROOMS (
                                        roomid integer PRIMARY KEY,
                                        location text NOT NULL
                                    );"""
        self.run_sql(sql_create_rooms_table)

        sql_create_schedules_table = """CREATE TABLE IF NOT EXISTS SCHEDULES (
                                        schedid integer PRIMARY KEY,
                                        classid integer NOT NULL,
                                        day integer NOT NULL,
                                        starttime integer NOT NULL,
                                        endtime integer NOT NULL,
                                        roomid integer NOT NULL,
                                        FOREIGN KEY (classid) REFERENCES CLASSES (classid),
                                        FOREIGN KEY (roomid) REFERENCES ROOMS (roomid)
                                    );"""
        self.run_sql(sql_create_schedules_table)

        sql_create_enrollments_table = """CREATE TABLE IF NOT EXISTS ENROLLMENTS (
                                        enrollid integer PRIMARY KEY,
                                        studentid integer NOT NULL,
                                        classid integer NOT NULL,
                                        status integer NOT NULL,
                                        enrolldate text NOT NULL,
                                        grade real,
                                        FOREIGN KEY (studentid) REFERENCES STUDENTS (studentid),
                                        FOREIGN KEY (classid) REFERENCES CLASSES (classid)
                                    );"""
        self.run_sql(sql_create_enrollments_table)

    def run_sql(self, sql):
        try:
            c = self.connection.cursor()
            c.execute(sql)
        except Error as e:
            print(e)

    def reset(self):
        self.run_sql("DROP TABLE IF EXISTS ENROLLMENTS")
        self.run_sql("DROP TABLE IF EXISTS SCHEDULES")
        self.run_sql("DROP TABLE IF EXISTS CLASSES")
        self.run_sql("DROP TABLE IF EXISTS ROOMS")
        self.run_sql("DROP TABLE IF EXISTS INSTRUCTORS")
        self.run_sql("DROP TABLE IF EXISTS PREREQS")
        self.run_sql("DROP TABLE IF EXISTS COURSES")
        self.run_sql("DROP TABLE IF EXISTS STUDENTS")
        self.run_sql("DROP TABLE IF EXISTS ADMINS")
        self.run_sql("DROP INDEX IF EXISTS idx_users_idno")
        self.run_sql("DROP TABLE IF EXISTS USERS")
        self.create_tables()
