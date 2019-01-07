import os
import sqlite3


def main():
    # create connection
    conn = sqlite3.connect('classes.db')
    count_iteration = 0
    while os.path.isfile('classes.db') & conn.execute("select * from courses").arraysize != 0:
        for course in total_table(conn):
            curr_class = check_if_id_exist(course[0], total_table(conn))
            # if timeLeft is zero
            if curr_class[3] == 0:
                # prints the command
                print('({}) {}: {} is schedule to start'.format(count_iteration, curr_class[1], course[1]))
                # update the current_course_id and the current_course_time_left in the current course
                conn.execute("update classrooms set current_course_id=?,current_course_time_left=? where id=?",
                             course[0], course[5], curr_class[0])
                conn.commit()
                # update the count in the current student type
                student = conn.execute("select * from students where grade=?", course[2])
                conn.execute("update students set count=? where grade=?", student[1]-course[3], course[2])
                conn.commit()
            else:
                # prints the command
                print('({}) {}: occupied by {}'.format(count_iteration, curr_class[1], course[1]))
                conn.execute("update classrooms set current_course_time_left=? where id = ?", course[5]-1, curr_class[0])
                conn.commit()
                # if course is done
                if course[5] == 0:
                    print('({}) {}: {} is done'.format(count_iteration, curr_class[1], course[1]))
                    conn.execute("update classrooms set current_course_id=? where id=?", 0, curr_class[0])
                    conn.commit()
                    conn.execute("delete from courses where id=?", course[0])
                    conn.commit()

            print_db(conn)
        count_iteration=count_iteration+1


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def print_db(conn):
    print("courses")
    print_table(conn.execute("select * from courses"))
    print("classrooms")
    print_table(conn.execute("select * from classrooms"))
    print("students")
    print_table(conn.execute("select * from students"))


def check_if_id_exist(id, classrooms_list):
    for curr_class in classrooms_list:
        if curr_class == id:
            return curr_class
    return None


def total_table(conn):
    return conn.execute("select * from courses as c join classrooms as cr on c.class_id=cr.id order by id")


if __name__ == "__main__":
    main()
