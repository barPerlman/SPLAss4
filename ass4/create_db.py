import sqlite3
import sys
from sqlite3 import Error
import re
import os
dbIsExist=os.path.isfile('schedule.db')


def main():
    if len(sys.argv) < 1 or sys.argv[1] is None:
        print("WRONG ARGUMENTS!!!")
        return
    if not dbIsExist:
        # create connection
        conn = create_db()
        if conn is not None:
            create_tables(conn)
            # get the config file to read
            conf_path = sys.argv[1]
            file = open(conf_path)
            content = file.read()
            splitted = content.split("\n")
            for line in splitted:  # insert tuple to db
                # check which table is it
                params = line.split(",")
                if line != '':
                    if params[0] == 'S':
                        insert_student(conn, params)
                    elif params[0] == 'C':
                        insert_course(conn, params)
                    else:
                        insert_classroom(conn, params)
            print_db(conn)
            conn.close()
    return


# method that is responsible to insert the tuple to students table
def insert_student(conn, params):
    for i in range (len(params)):
        params[i] = remove_spaces(params[i])
    studentGrade = conn.cursor().execute("SELECT grade FROM students WHERE grade=?", (params[1],)).fetchone()
    if studentGrade is None:
        conn.execute("INSERT INTO students (grade,count) VALUES (?,?)", [params[1], params[2]])
        conn.commit()


# method that is responsible to insert the tuple to courses table
def insert_course(conn, params):
    for i in range (len(params)):
        params[i] = remove_spaces(params[i])
    courseId = conn.cursor().execute("SELECT id FROM courses WHERE id=?", (params[1],)).fetchone()
    if courseId is None:
        conn.execute("INSERT INTO courses (id,course_name,student,number_of_students,class_id,course_length) VALUES (?,?,?,?,?,?)",
                 [params[1], params[2], params[3], params[4], params[5], params[6]])
        conn.commit()


# method that is responsible to insert the tuple to classrooms table
def insert_classroom(conn, params):
    for i in range (len(params)):
        params[i] = remove_spaces(params[i])
    classroomId = conn.cursor().execute("SELECT id FROM classrooms WHERE id=?", (params[1],)).fetchone()
    if classroomId is None:
        conn.execute("INSERT INTO classrooms (id,location,current_course_id,current_course_time_left) VALUES (?,?,?,?)",
                 [params[1], params[2], 0, 0])
        conn.commit()


# method that is responsible to remove spaces from a tuple
def remove_spaces(word):
    first_index=-1
    second_index=-1
    match=re.search(r'[^ ]', word)
    if match:
        first_index=match.start()
        i=len(word)-1
        while word[i]==' ':
            i=i-1
        second_index=i
    word=word[first_index:second_index+1]
    return word


# method that is responsible to remove create the database if it's not exists
def create_db():
    try:
        conn = sqlite3.connect('schedule.db')
        return conn
    except Error as e:
        print(e)
    return None


# method that is responsible to create tables if they are not exists
def create_tables(conn):
    conn.executescript(""" 
        CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        student TEXT NOT NULL,
        number_of_students INTEGER NOT NULL,
        class_id INTEGER REFERENCES classrooms(id),
        course_length INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS students (
        grade TEXT PRIMARY KEY,
        count INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS classrooms (
        id INTEGER PRIMARY KEY,
        location TEXT NOT NULL,
        current_course_id INTEGER NOT NULL,
        current_course_time_left INTEGER NOT NULL
        );
    """)


# method that is responsible to print the database
def print_db(conn):
    print("courses")
    print_table(conn.execute("select * from courses"))
    print("classrooms")
    print_table(conn.execute("select * from classrooms"))
    print("students")
    print_table(conn.execute("select * from students"))


# method that is responsible to print a table
def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


# calls to the main function
if __name__ == "__main__":
    main()
