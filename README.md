# comet-sys
Sample text-based enlistment/enrollment system.

Part of the requirements for the COMET Term 1 Project.

## How to use

If you want to reset the database, just remove the file `cometsys.db` in the
root directory. When the database is reset, the program automatically adds a
default admin user whose username is `year0001` (e.g. `20190001`) and password
is `password`.

## Features

* Log in as either a student or an admin
* Enlist in and drop from different classes
* Prerequisites (cannot enlist without enlisting in its prerequisites)
* Admins can create, edit, view and delete courses, as well as classes for them
* Courses can be academic or non-academic; non-academic courses won't add up to
  the student's load
* The system is implemented using a Sqlite3 database.

## Notes

* Rooms must be created before classes can be created to prevent excessive typing.
