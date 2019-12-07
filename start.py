# entry point for the enlistment system application

from database import Database
from model.cclass import Instructor, Room
from model.user import User, Admin, Student, UserType
from model.course import Course

def student_main(db : Database, student : Student):
    print("Welcome, " + student.get_first() + " " + student.get_middle() + " " + student.get_last())

    running = True
    while running:
        print("(1) Enlist in class")
        print("(2) Drop class")
        print("(3) View enlistment")
        print("(4) Change password")
        print("(5) Log out")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            term = int(input("Enter term: "))
            current_load = db.get_student_load(student, term)
            print("Your load: " + str(current_load) + ".0 units")
            all_classes = db.get_all_classes(term)
            print("{0:3}  {1:15}{2:10}{3:35}{4:10}{5:10}{6:15}".format("#", "Course Code", "Section", "Instructor", "Room", "Units", "Occupancy"))
            ctr = 1
            for cp in all_classes:
                c = cp[0]
                count = cp[1]
                cs = c.get_course()
                ccode = cs.get_course_code()
                i = c.get_instructor()
                iname = "" if i is None else "{}, {} {}".format(i.get_last(), i.get_first(), i.get_middle())
                r = c.get_room()
                rloc = r.get_location()
                ustr = str(cs.get_units()) + ".0" if cs.is_academic() else "(" + str(cs.get_units()) + ".0)"
                print("{0:3}  {1:15}{2:10}{3:35}{4:10}{5:10}{6:15}".format(ctr, ccode, c.get_section(), iname, rloc, ustr, str(count) + "/" + str(c.get_class_limit())))
                ctr = ctr + 1

            ch = int(input("Select class: "))
            if ch >= 1 and ch <= len(all_classes):
                clazz = all_classes[ch - 1][0]
                prereqs = db.get_prerequisites(clazz.get_course())
                
                proceed = True
                for req in prereqs:
                    if not proceed:
                        break
                    else:
                        proceed = db.has_student_enrolled(student, req.get_id(), clazz.term)

                if proceed:
                    count = db.count_enrolled(clazz)
                    if count < clazz.get_class_limit():
                        if not cs.is_academic() or current_load + cs.get_units() <= student.get_limit():
                            db.enlist(student, clazz)
                        else:
                            print("You're overloaded this term!")
                    else:
                        print("This class is already full!")
                else:
                    print("You have not completed the prerequisites for this course!")
            elif ch != 0:
                print("Invalid class")

        elif choice == 2:
            term = int(input("Enter term: "))
            enrollments = db.get_student_enrollment(student, term)
            print("{0:3}  {1:15}{2:10}{3:35}{4:10}{5:10}".format("#", "Course Code", "Section", "Instructor", "Room", "Units"))

            ctr = 1
            for e in enrollments:
                c = e.get_class()
                cs = c.get_course()
                ccode = cs.get_course_code()
                i = c.get_instructor()
                iname = "" if i is None else "{}, {} {}".format(i.get_last(), i.get_first(), i.get_middle())
                r = c.get_room()
                rloc = r.get_location()
                ustr = str(cs.get_units()) + ".0" if cs.is_academic() else "(" + str(cs.get_units()) + ".0)"
                print("{0:3}  {1:15}{2:10}{3:35}{4:10}{5:10}".format(ctr, ccode, c.get_section(), iname, rloc, ustr))
                ctr = ctr + 1

            ch = int(input("Select class: "))
            if ch >= 1 and ch <= len(all_classes):
                db.drop(student, e[ch - 1].get_class())
            elif ch != 0:
                print("Invalid class")

        elif choice == 3:
            term = int(input("Enter term: "))
            enrollments = db.get_student_enrollment(student, term)
            print("{0:15}{1:10}{2:35}{3:10}{4:10}".format("Course Code", "Section", "Instructor", "Room", "Units"))
            for e in enrollments:
                c = e.get_class()
                cs = c.get_course()
                ccode = cs.get_course_code()
                i = c.get_instructor()
                iname = "" if i is None else "{}, {} {}".format(i.get_last(), i.get_first(), i.get_middle())
                r = c.get_room()
                rloc = r.get_location()
                ustr = str(cs.get_units()) + ".0" if cs.is_academic() else "(" + str(cs.get_units()) + ".0)"
                print("{0:15}{1:10}{2:35}{3:10}{4:10}".format(ccode, c.get_section(), iname, rloc, ustr))

        elif choice == 4:
            password = input("Verify password: ")
            verify = db.login(student.get_id(), password)
            if verify is not None:
                newpass = input("Enter new password: ")
                db.edit_password(student.get_id(), newpass)
            else:
                print("Cannot verify user")
        elif choice == 5:
            running = False
        else:
            print("Invalid choice")

def admin_choose_instructor(db : Database):
    insts = db.get_instructors()
    ctr = 1
    print("(0) Cancel")
    for i in insts:
        print("(" + str(ctr) + ") " + i.get_last() + ", " + i.get_first() + " " + i.get_middle())
        ctr = ctr + 1
    ch = int(input("Select instructor: "))
    if ch >= 1 and ch <= len(insts):
        return insts[ch - 1]
    elif ch != 0:
        print("Invalid instructor")
    return None

def admin_choose_course(db : Database):
    ccode = input("Enter course code: ")
    course = db.get_course(ccode)
    if course is not None:
        return course
    else:
        print("Not a valid course")
        return None

def admin_choose_class(db : Database):
    course = admin_choose_course(db)
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
                return classes[ch - 1]
            else:
                print("Invalid class")
        else:
            print("There are no classes for this course")
    return None

def admin_choose_room(db : Database):
    rooms = db.get_rooms()
    ctr = 1
    print("(0) Cancel")
    for i in rooms:
        print("(" + str(ctr) + ") " + i.get_location())
        ctr = ctr + 1
    ch = int(input("Select room: "))
    if ch >= 1 and ch <= len(rooms):
        return rooms[ch - 1]
    elif ch != 0:
        print("Invalid room")
    return None


def admin_accounts(db : Database, admin : Admin):
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
            load = int(input("Enter max units: "))
            db.new_student(idno, "", last, first, middle, load)
        
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


def admin_courses(db : Database, admin : Admin):
    running = True
    while running:
        print("(1) Add course")
        print("(2) Set prerequisite")
        print("(3) Clear prerequisites")
        print("(4) View courses")
        print("(5) Remove course")
        print("(6) Create class")
        print("(7) Assign instructor to class")
        print("(8) View classes for course")
        print("(9) Delete class")
        print("(10) Go back")

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
                    db.new_prerequisite(course, prereqc)
                else:
                    print("No course found")
            else:
                print("No course found")
        elif choice == 3:
            code = input("Enter course code: ")
            course = db.get_course(code)
            if course is not None:
                db.clear_prerequisites(course)
            else:
                print("No course found")
        elif choice == 4:
            courses = db.get_courses()
            print("{0:16}{1:56}{2:8}".format("Course code", "Course name", "Units"))
            for course in courses:
                units = course.get_units()
                ccode = course.get_course_code()
                cname = course.get_name()
                print("{0:16}{1:56}{2:8}".format(ccode, cname, str(units) + ".0" if course.is_academic() else "(" + str(units) + ".0)"))
            print()
        elif choice == 5:
            code = input("Enter course code to delete: ")
            db.delete_course(code)
        elif choice == 6:
            ccode = input("Enter course code for new class: ")
            course = db.get_course(ccode)
            if course is not None:
                section = input("Enter section name: ")
                term = int(input("Enter term (year/term): "))
                classlimit = input("Enter class limit: ")
                room = admin_choose_room(db)
                if room is not None:
                    db.new_class(course, section, term, room, classlimit)
                else:
                    print("Invalid room")            
            else:
                print("Not a valid course")
        elif choice == 7:
            clazz = admin_choose_class(db)
            if clazz is not None:
                inst = admin_choose_instructor(db)
                if inst is not None:
                    db.assign_instructor(clazz.get_id(), inst)
        elif choice == 8:
            course = admin_choose_course(db)
            if course is not None:
                term = int(input("Enter term: "))
                classes = db.get_classes(course, term)
                if len(classes) > 0:
                    print("{0:10}{1:40}".format("Section", "Instructor"))
                    for c in classes:
                        i = c.get_instructor()
                        print("{0:10}{1:40}".format(c.get_section(), "{}, {} {}".format(i.get_last(), i.get_first(), i.get_middle())))
                else:
                    print("There are no classes for this course")
        elif choice == 9:
            clazz = admin_choose_class(db)
            if clazz is not None:
                db.delete_class(clazz.get_id())
        elif choice == 10:
            running = False
        else:
            print("Invalid choice")

def admin_rooms(db : Database, admin : Admin):
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
            room = admin_choose_room(db)
            if room is not None:
                if db.delete_room(room.get_location()):
                    print("Successfully removed room")
                else:
                    print("Nothing was removed")
        elif choice == 4:
            running = False
        else:
            print("Invalid choice")

def admin_instructors(db : Database, admin : Admin):
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

def admin_main(db : Database, admin : Admin):
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
