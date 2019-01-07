import sqlite3
import sys
import os
from sqlite3 import Error


def main():
    df=sys.argv[2]
    if len(sys.argv) < 1:
        print("NOT ENOUGH ARGUMENTS!")
        return
    elif sys.argv[2]=="classes.db":
        # create connection
        conn = create_db()
        if not conn is None:
            create_tables(conn)
            # get the config file to read
            conf_path = sys.argv[1]
            file = open(conf_path)
            content = file.read()
            splitted = content.split("\n")
            for line in splitted:  # insert tuple to db
                # check which table is it
                params = line.split(", ")
                if params[0] == 'S':
                    insert_student(conn, params)
                elif params[0] == 'C':
                    insert_course(conn, params)
                else:
                    insert_classroom(conn, params)
            print_db(conn)
            conn.close()
    return


def insert_student(conn, params):
    conn.execute("""
        INSERT INTO students (grade,count) VALUES (?,?)""", [params[1], params[2]])


def insert_course(conn, params):
    conn.execute("""
        INSERT INTO courses (id,course_name,student,number_of_students,class_id,course_length) VALUES (?,?,?,?,?,?)""",
                 [params[1], params[2], params[3], params[4], params[5], params[6]])


def insert_classroom(conn, params):
    conn.execute("""
        INSERT INTO classrooms (id,location,current_course_id,current_course_time_left) VALUES (?,?,?,?)""",
                 [params[1], params[2], params[3], params[4]])


def create_db():
    try:
        conn = sqlite3.connect('classes.db')
        return conn
    except Error as e:
        print(e)
    return None


def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXIST courses (
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        student TEXT NOT NULL,
        number_of_students INTEGER NOT NULL,
        class_id INTEGER REFERENCES classrooms(id),
        course_length INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXIST students (
        grade TEXT PRIMARY KEY,
        count INTEGER NOT NULL
        );
        
        CREATE TABLE IF NOT EXIST classrooms (
        id INTEGER PRIMARY KEY,
        location TEXT NOT NULL,
        current_course_id INTEGER NOT NULL,
        current_course_time_left INTEGER NOT NULL
        );
    """)

def print_db(conn):
    print("courses")
    print_table(conn.execute("select * from courses"))
    print("classrooms")
    print_table(conn.execute("select * from classrooms"))
    print("students")
    print_table(conn.execute("select * from students"))


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


if __name__ == "__main__":
    main()
