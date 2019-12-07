# entry point for the enlistment system application

from database import Database
from model.cclass import Instructor, Room
from model.user import User, UserType
from model.course import Course



def student_main(db : Database, student : User):
    print("Welcome, " + student.get_first() + " " + student.get_middle() + " " + student.get_last())

    running = True
    while running:
        print("(1) Enlist in class")
        print("(2) Drop class")
        print("(3) View enlistment")
        print("(4) View schedule")
        print("(5) Change password")
        print("(6) Log out")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            pass
        elif choice == 6:
            running = False
        else:
            print("Invalid choice")

def admin_accounts(db : Database, admin : User):
    running = True
    while running:
        print("(1) New admin account")
        print("(2) New student account")
        print("(3) Change name")
        print("(4) Change password")
        print("(5) Change student's name")
        print("(6) Change student's password")
        print("(7) Go back")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            idno = int(input("Enter ID number: "))
            last = input("Enter last name: ")
            first = input("Enter first name: ")
            middle = input("Enter middle name: ")
            db.new_admin(idno, "", last, first, middle)

        elif choice == 2:
            idno = int(input("Enter ID number: "))
            last = input("Enter last name: ")
            first = input("Enter first name: ")
            middle = input("Enter middle name: ")
            db.new_student(idno, "", last, first, middle)
        
        elif choice == 3:
            password = input("Verify password: ")
            verify = db.login(admin.get_id(), password)
            if verify is not None:
                last = input("Enter last name: ")
                first = input("Enter first name: ")
                middle = input("Enter middle name: ")
                db.edit_user(admin.get_id(), last, first, middle)
            else:
                print("Cannot verify user")
        
        elif choice == 4:
            password = input("Verify password: ")
            verify = db.login(admin.get_id(), password)
            if verify is not None:
                newpass = input("Enter new password: ")
                db.edit_password(admin.get_id(), newpass)
            else:
                print("Cannot verify user")
        
        elif choice == 5:
            verify = db.login(admin.get_id(), password)
            if verify is not None:
                idno = int(input("Enter ID of student: "))
                student = db.get_user(idno)

                if student is not None:
                    if student.get_type() == UserType.STUDENT:
                        last = input("Enter last name: ")
                        first = input("Enter first name: ")
                        middle = input("Enter middle name: ")
                        db.edit_user(idno, last, first, middle)
                    else:
                        print("User is not a student")
                else:
                    print("No user with ID " + str(idno) + " exists")
            else:
                print("Cannot verify user")
        
        elif choice == 6:
            verify = db.login(admin.get_id(), password)
            if verify is not None:
                idno = int(input("Enter ID of student: "))
                student = db.get_user(idno)

                if student is not None:
                    if student.get_type() == UserType.STUDENT:
                        newpass = input("Enter new password: ")
                        db.edit_password(idno, newpass)
                    else:
                        print("User is not a student")
                else:
                    print("No user with ID " + str(idno) + " exists")
            else:
                print("Cannot verify user")

        elif choice == 7:
            running = False
        else:
            print("Invalid choice")


def admin_courses(db : Database, admin : User):
    running = True
    while running:
        print("(1) Add course")
        print("(2) Set prerequisite")
        print("(3) View courses")
        print("(4) Remove course")
        print("(5) Create class")
        print("(6) Assign instructor to class")
        print("(7) View classes for course")
        print("(8) Delete class")
        print("(9) View enrollment")
        print("(10) Create schedule for class")
        print("(11) View schedule for class")
        print("(12) Delete schedule for class")
        print("(13) Go back")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            code = input("Enter course code: ")
            name = input("Enter course name: ")
            units = int(input("Enter number of units: "))
            is_academic = input("Enter (Y/n) if academic: ") == "Y"
            db.new_course(code, name, units, is_academic)
        elif choice == 2:
            code = input("Enter course code: ")
            course = db.get_course(code)
            if course is not None:
                prereq = input("Enter prerequisite: ")
                prereqc = db.get_course(prereq)
                if prereqc is not None:
                    print("(1) Hard prerequisite")
                    print("(2) Soft prerequisite")
                    type = int(input("Enter type: "))
                    if type >= 1 and type <= 2:
                        db.new_prerequisite(course, prereqc, type)
                    else:
                        print("Invalid type")
                else:
                    print("No course found")
            else:
                print("No course found")
        elif choice == 3:
            courses = db.get_courses()
            print("{0:16}{1:40}{2:8}".format("Course code", "Course name", "Units"))
            for course in courses:
                units = course.get_units()
                ccode = course.get_course_code()
                cname = course.get_name()
                print("{0:16}{1:40}{2:8}".format(ccode, cname, str(units) + ".0" if course.is_academic() else "(" + str(units) + ".0)"))
            print()
        elif choice == 4:
            code = input("Enter course code to delete: ")
            db.delete_course(code)
        elif choice == 5:
            ccode = input("Enter course code for new class: ")
            course = db.get_course(ccode)
            if course is not None:
                section = input("Enter section name: ")
                term = int(input("Enter term (year/term): "))
                classlimit = input("Enter class limit: ")
                db.new_class(course, section, term, classlimit)
            else:
                print("Not a valid course")
        elif choice == 6:
            ccode = input("Enter course code: ")
            course = db.get_course(ccode)
            if course is not None:
                term = int(input("Enter term: "))
                classes = db.get_classes(course, term)
                if len(classes) > 0:
                    ctr = 1
                    for c in classes:
                        print("(" + str(ctr) + ") " + c.get_section())
                        ctr = ctr + 1
                    ch = int(input("Select class: "))
                    if ch >= 1 and ch <= len(classes):
                        insts = db.get_instructors()
                        ctr = 1
                        for i in insts:
                            print("(" + str(ctr) + ") " + i.get_last() + ", " + i.get_first() + " " + i.get_middle())
                            ctr = ctr + 1
                        ch2 = int(input("Select instructor: "))
                        if ch2 >= 1 and ch2 <= len(insts):
                            db.assign_instructor(classes[ch - 1].get_id(), insts[ch2 - 1])
                        else:
                            print("Invalid instructor")
                    else:
                        print("Invalid class")
                else:
                    print("There are no classes for this course")
            else:
                print("Not a valid course")
        elif choice == 7:
            ccode = input("Enter course code: ")
            course = db.get_course(ccode)
            if course is not None:
                term = int(input("Enter term: "))
                classes = db.get_classes(course, term)
                if len(classes) > 0:
                    for c in classes:
                        print(c.get_section())
                else:
                    print("There are no classes for this course")
            else:
                print("Not a valid course")
        elif choice == 8:
            ccode = input("Enter course code: ")
            course = db.get_course(ccode)
            if course is not None:
                term = int(input("Enter term: "))
                classes = db.get_classes(course, term)
                if len(classes) > 0:
                    ctr = 1
                    for c in classes:
                        print("(" + str(ctr) + ") " + c.get_section())
                        ctr = ctr + 1
                    ch = int(input("Select class: "))
                    if ch >= 1 and ch <= len(classes):
                        db.delete_class(c.get_id())
                    else:
                        print("Invalid class")
                else:
                    print("There are no classes for this course")
            else:
                print("Not a valid course")
        elif choice == 9:
            pass
        elif choice == 13:
            running = False
        else:
            print("Invalid choice")

def admin_rooms(db : Database, admin : User):
    running = True
    while running:
        print("(1) Add room")
        print("(2) View rooms")
        print("(3) Remove room")
        print("(4) Go back")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            location = input("Enter room label: ")
            db.new_room(location)
        elif choice == 2:
            rooms = db.get_rooms()
            print("All rooms:")
            for room in rooms:
                print(room.get_location())
            print()
        elif choice == 3:
            location = input("Enter location of room: ")
            if db.delete_room(location):
                print("Successfully removed room")
            else:
                print("Nothing was removed")
        elif choice == 4:
            running = False
        else:
            print("Invalid choice")

def admin_instructors(db : Database, admin : User):
    running = True
    while running:
        print("(1) Add instructor")
        print("(2) Edit instructor info")
        print("(3) View instructors")
        print("(4) Remove instructor")
        print("(5) Go back")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            idno = int(input("Enter ID number: "))
            last = input("Enter last name: ")
            first = input("Enter first name: ")
            middle = input("Enter middle name: ")
            db.new_instructor(idno, last, first, middle)

        elif choice == 2:
            idno = int(input("Enter ID number of instructor: "))
            inst : Instructor = db.get_instructor(idno)
            if inst is not None:
                print("Old name is " + inst.get_last() + ", " + inst.get_first() + " " + inst.get_middle())
                last = input("Enter last name: ")
                first = input("Enter first name: ")
                middle = input("Enter middle name: ")
                db.edit_instructor(idno, last, first, middle)
            else:
                print("No instructor with ID " + str(idno) + " found.")

        elif choice == 3:
            insts = db.get_instructors()
            print("{0:40}{1:10}".format("Instructor name", "ID number"))
            for inst in insts:
                print("{0:40}{1:10}".format("{}, {} {}".format(inst.get_last(), inst.get_first(), inst.get_middle()), inst.get_id()))
            print()

        elif choice == 4:
            idno = int(input("Enter ID number of instructor: "))
            if db.delete_instructor(idno):
                print("Successfully removed instructor")
            else:
                print("Nothing was removed")

        elif choice == 5:
            running = False
        else:
            print("Invalid choice")

def admin_main(db : Database, admin : User):
    print("Welcome, " + admin.get_first() + " " + admin.get_middle() + " " + admin.get_last())

    running = True
    while running:
        print("(1) User registration and account management")
        print("(2) Courses and enrollment")
        print("(3) Rooms")
        print("(4) Instructors")
        print("(5) Log out")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            admin_accounts(db, admin)
        elif choice == 2:
            admin_courses(db, admin)
        elif choice == 3:
            admin_rooms(db, admin)
        elif choice == 4:
            admin_instructors(db, admin)
        elif choice == 5:
            running = False
        else:
            print("Invalid choice")


def main():
    db = Database("cometsys.db")

    running = True
    while running:
        print("(1) Log in")
        print("(2) Exit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            idno = int(input("Enter your ID number: "))
            password = input("Enter your password: ")
            user = db.login(idno, password)
            if user is not None:
                if user.get_type() == UserType.ADMIN:
                    admin_main(db, user)
                else:
                    student_main(db, user)
            else:
                print("Invalid ID number or password")
        elif choice == 2:
            running = False
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
