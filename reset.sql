DROP TABLE IF EXISTS ENROLLMENTS;
DROP TABLE IF EXISTS SCHEDULES;
DROP TABLE IF EXISTS CLASSES;
DROP TABLE IF EXISTS ROOMS;
DROP TABLE IF EXISTS INSTRUCTORS;
DROP TABLE IF EXISTS PREREQS;
DROP TABLE IF EXISTS COURSES;
DROP TABLE IF EXISTS STUDENTS;
DROP TABLE IF EXISTS ADMINS;
DROP TABLE IF EXISTS USERS;

CREATE TABLE IF NOT EXISTS USERS (
    idno            INTEGER PRIMARY KEY,
    lastname        TEXT NOT NULL,
    firstname       TEXT NOT NULL,
    middlename      TEXT NOT NULL,
    type            INTEGER NOT NULL,
    password        TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS STUDENTS (
    idno            INTEGER PRIMARY KEY,
    FOREIGN KEY (idno) REFERENCES USERS (idno)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS ADMINS (
    idno            INTEGER PRIMARY KEY,
    FOREIGN KEY (idno) REFERENCES USERS (idno)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS COURSES (
    courseid        INTEGER PRIMARY KEY,
    coursecode      TEXT NOT NULL UNIQUE,
    name            TEXT NOT NULL,
    units           INTEGER NOT NULL,
    is_academic     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS PREREQS (
    courseid        INTEGER PRIMARY KEY,
    prerequisite    INTEGER NOT NULL,
    type            INTEGER NOT NULL,
    FOREIGN KEY (courseid)      REFERENCES COURSES (courseid) ON DELETE CASCADE,
    FOREIGN KEY (prerequisite)  REFERENCES COURSES (courseid) ON DELETE CASCADE,
    UNIQUE (courseid, prerequisite)
);

CREATE TABLE IF NOT EXISTS INSTRUCTORS (
    idno            INTEGER PRIMARY KEY,
    lastname        TEXT NOT NULL,
    firstname       TEXT NOT NULL,
    middlename      TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS CLASSES (
    classid         INTEGER PRIMARY KEY,
    courseid        INTEGER NOT NULL,
    section         TEXT NOT NULL,
    term            INTEGER NOT NULL,
    instructor      INTEGER NOT NULL,
    classlimit      INTEGER NOT NULL,
    FOREIGN KEY (courseid)      REFERENCES COURSES (courseid),
    FOREIGN KEY (instructor)    REFERENCES INSTRUCTORS (idno)
    UNIQUE (courseid, section, term)
);

CREATE TABLE IF NOT EXISTS ROOMS (
    roomid          INTEGER PRIMARY KEY,
    location        TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS SCHEDULES (
    schedid         INTEGER PRIMARY KEY,
    classid         INTEGER NOT NULL,
    day             INTEGER NOT NULL,
    starttime       INTEGER NOT NULL,
    endtime         INTEGER NOT NULL,
    roomid          INTEGER NOT NULL,
    FOREIGN KEY (classid)   REFERENCES CLASSES (classid),
    FOREIGN KEY (roomid)    REFERENCES ROOMS (roomid)
);

CREATE TABLE IF NOT EXISTS ENROLLMENTS (
    enrollid        INTEGER PRIMARY KEY,
    studentid       INTEGER NOT NULL,
    classid         INTEGER NOT NULL,
    status          INTEGER NOT NULL,
    enrolldate      TEXT NOT NULL,
    grade           REAL,
    FOREIGN KEY (studentid) REFERENCES STUDENTS (idno),
    FOREIGN KEY (classid)   REFERENCES CLASSES (classid) ON DELETE CASCADE
    UNIQUE (studentid, classid)
);
