import os
dbIsExist=os.path.isfile('schedule.db')
import sqlite3


def main():
    # create connection
    conn = create_db()
    cursor = conn.cursor()
    count_iteration = 0
    if dbIsExist and len(conn.cursor().execute("SELECT * FROM courses").fetchall())==0:
        print_db(conn)
    else :
        while dbIsExist and conn.cursor().execute("SELECT * FROM courses").fetchall():
            list = total_table(cursor)
            i=0
            while i<len(list):
                curr_class = total_table(conn)[i]
                if curr_class is not None:
                    if curr_class[9] == 0:
                        # prints the command
                        print('({}) {}: {} is schedule to start'.format(count_iteration, curr_class[7], curr_class[1]))
                        # update the current_course_id and the current_course_time_left in the current course
                        conn.execute("UPDATE classrooms SET current_course_id=?,current_course_time_left=? WHERE id=?",
                                     [curr_class[0], curr_class[5], curr_class[6]])
                        conn.commit()
                        # update the count in the current student type
                        student = conn.cursor().execute("SELECT * FROM students WHERE grade=?", (curr_class[2],)).fetchone()
                        conn.execute("UPDATE students SET count=? WHERE grade=?", [student[1]-curr_class[3], curr_class[2]])
                        conn.commit()
                    else:
                        # if course is done
                        if curr_class[9]-1 == 0:
                            print('({}) {}: {} is done'.format(count_iteration, curr_class[7], curr_class[1]))
                            # update the current_course_id in the current classroom
                            conn.execute("UPDATE classrooms SET current_course_id=? WHERE id=?", [0, curr_class[6]])
                            conn.commit()
                            # update the current_course_time_left in the current classroom
                            conn.execute("UPDATE classrooms SET current_course_time_left=? WHERE id=?", [0, curr_class[6]])
                            conn.commit()
                            # delete the course in the courses table
                            conn.execute("DELETE FROM courses WHERE class_id=? and id=?", [curr_class[4],curr_class[0]])
                            conn.commit()
                            list=total_table(cursor)
                            i=i-1
                        else :
                            # prints the command
                            print('({}) {}: occupied by {}'.format(count_iteration, curr_class[7], curr_class[1]))
                            # update the current_course_time_left in the current classroom
                            conn.execute("UPDATE classrooms SET current_course_time_left=? WHERE id = ?",
                                         [curr_class[9] - 1, curr_class[6]])
                            conn.commit()
                    i=i+1
            # prints the database
            print_db(conn)
            count_iteration=count_iteration+1


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


# method that is responsible to return the current courses that are in handel
def total_table(cursor):
    return cursor.execute("""SELECT * FROM courses as c INNER JOIN classrooms as cr ON c.class_id=cr.id WHERE NOT 
        EXISTS (SELECT * FROM courses WHERE class_id=c.class_id AND id<c.id) ORDER BY class_id""").fetchall()


# method that is responsible to remove create the database if it's not exists
def create_db():
    try:
        conn = sqlite3.connect('schedule.db')
        return conn
    except sqlite3.Error as e:
        print(e)
    return None


# calls to the main function
if __name__ == "__main__":
    main()
