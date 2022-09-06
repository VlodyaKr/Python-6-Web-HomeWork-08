import datetime
import sqlite3 as sql
import os
from random import randint

from faker import Faker


def insert_tables():
    if os.path.exists('univer.db'):
        fake = Faker()
        with sql.connect('univer.db') as conn:
            cur = conn.cursor()
            # DB students
            cur.execute('DELETE FROM students')
            cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "students"')
            conn.commit()
            for _ in range(30):
                cur.execute("INSERT INTO students(name) VALUES(?)", (fake.name(),))

            # DB teachers
            cur.execute('DELETE FROM teachers')
            cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "teachers"')
            conn.commit()
            for _ in range(3):
                cur.execute("INSERT INTO teachers(name) VALUES(?)", (fake.name(),))

            # DB subjects
            subject_list = ['Python', 'C++', 'C#', 'Java', 'JavaScript']
            cur.execute('DELETE FROM subjects')
            cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "subjects"')
            conn.commit()
            for subject in subject_list:
                cur.execute("INSERT INTO subjects(name) VALUES(?)", (subject,))

            # DB groups
            group_list = ['Gr.11', 'Gr.12', 'Gr.13']
            cur.execute('DELETE FROM groups')
            cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "groups"')
            conn.commit()
            for group in group_list:
                cur.execute("INSERT INTO groups(name) VALUES(?)", (group,))

            # DB groups_of_students
            cur.execute('DELETE FROM groups_of_students')
            conn.commit()
            for i_st in range(30):
                cur.execute("INSERT INTO groups_of_students(id_group, id_student) VALUES(?, ?)", ((i_st // 10) + 1, i_st + 1))

            # DB teachers_subjects
            cur.execute('DELETE FROM teachers_subjects')
            teacher_subject = [(1, 1), (2, 2), (2, 3), (3, 4), (3, 5)]
            conn.commit()
            for t_sub in teacher_subject:
                cur.execute("INSERT INTO teachers_subjects(id_teacher, id_subject) VALUES(?, ?)", t_sub)

            # DB teachers_subjects
            cur.execute('DELETE FROM subjects_in_groups')
            conn.commit()
            for i_gr in range(3):
                for i_sub in range(5):
                    cur.execute("INSERT INTO subjects_in_groups(id_group, id_subject) VALUES(?, ?)", (i_gr + 1, i_sub + 1))

            # DB grades
            cur.execute('DELETE FROM grades')
            cur.execute('UPDATE sqlite_sequence SET seq = 0 WHERE name = "grades"')
            conn.commit()
            for i_st in range(30):
                for i_sub in range(5):
                    for _ in range(4):
                        cur.execute("INSERT INTO grades(id_student, id_subject, grade, grade_date) VALUES(?, ?, ?, ?)",
                                    (i_st + 1, i_sub + 1, randint(1, 12), datetime.datetime.now().date() -
                                     datetime.timedelta(days=randint(0, 100))))

            cur.close()
        print('DB is completed\n')
    else:
        print('DB not exist. Press "1 - creation of tables2"\n')
