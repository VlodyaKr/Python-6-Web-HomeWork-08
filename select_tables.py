import os
import sqlite3 as sql
from random import randint


def select_tables():
    if os.path.exists('univer.db'):
        with sql.connect('univer.db') as conn:
            cur = conn.cursor()

            # Is empty
            cur.execute("SELECT * FROM teachers")
            rows = cur.fetchall()
            if not rows:
                print('DB is empty. Press "2 - completing tables"\n')
                return

            # Report 1
            print('\n----- Report 1 ----- 5 students with the highest average score in all subjects')
            title = ['av.grade', 'student']
            print(f'| {title[0]:^8} | {title[1]:^30} |')
            cur.execute("""SELECT AVG(grade) AS av_grade, name AS student FROM grades g
                JOIN students s ON g.id_student = s.id  
                GROUP BY id_student 
                ORDER BY av_grade DESC 
                LIMIT 5;""")
            rows = cur.fetchall()
            for row in rows:
                print(f'|{row[0]:^10.2f}| {row[1]:<30} |')

            # Report 2
            print(f'\n----- Report 2 ----- 1 student with the highest average score in one subject')
            title = ['subject', 'student', 'max.grade']
            print(f'| {title[0]:^15} | {title[1]:^30} | {title[2]:^10} |')
            cur.execute(f"""SELECT s.name AS subject, st.name AS student, AVG(grade) AS av_grade FROM grades g 
                JOIN subjects s ON g.id_subject = s.id
                JOIN students st ON g.id_student = st.id 
                WHERE id_subject = {randint(1, 5)}
                GROUP BY id_student 
                ORDER BY av_grade DESC 
                LIMIT 1;""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:<15} | {row[1]:<30} | {row[2]:^10.2f} |')

            # Report 3
            print(f'\n----- Report 3 ----- average score in a group for one subject')
            title = ['subject', 'group', 'av.grade']
            print(f'| {title[0]:^15} | {title[1]:^5} | {title[2]:^10} |')
            cur.execute(f"""SELECT s.name AS subject, gr.name AS group_name, AVG(grade) av_grade FROM grades g 
                JOIN subjects s ON g.id_subject = s.id
                JOIN students st ON g.id_student = st.id 
                JOIN groups_of_students gos ON g.id_student = gos.id_student 
                JOIN groups gr ON gos.id_group = gr.id  
                WHERE id_subject = {randint(1, 5)}
                GROUP BY gos.id_group;""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:<15} | {row[1]:<5} | {row[2]:^10.2f} |')

            # Report 4
            print(f'\n----- Report 4 ----- grade point average in stream')
            title = ['av.grade']
            print(f'| {title[0]:^10} |')
            cur.execute("SELECT AVG(grade) AS av_grade FROM grades g;")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:^10.2f} |')

            # Report 5
            print(f'\n----- Report 5 ----- what courses does the teacher teach')
            title = ['teacher', 'subject']
            print(f'| {title[0]:^30} | {title[1]:^15} |')
            cur.execute(f"""SELECT t.name AS teacher, s.name AS subject FROM teachers_subjects ts 
                JOIN teachers t ON id_teacher = t.id 
                JOIN subjects s ON id_subject =s.id 
                WHERE id_teacher = {randint(1, 3)};""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:<30} | {row[1]:<15} |')

            # Report 6
            print(f'\n----- Report 6 ----- list of students in the group')
            title = ['group', 'student']
            print(f'| {title[0]:^5} | {title[1]:^30} |')
            cur.execute(f"""SELECT g.name AS group_name, s.name AS student FROM groups_of_students gos 
                JOIN students s ON id_student = s.id 
                JOIN groups g ON id_group = g.id 
                WHERE id_group = {randint(1, 3)}
                ORDER BY student;""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:^5} | {row[1]:<30} |')

            # Report 7
            print(f'\n----- Report 7 ----- grades of students in the subject group')
            title = ['group', 'subject', 'student', 'grade', 'date']
            print(f'| {title[0]:^5} | {title[1]:^15} | {title[2]:^30} | {title[3]:^5} | {title[4]:^10} |')
            cur.execute(f"""SELECT gr.name AS group_name, s.name AS subject, st.name AS student, g.grade AS grade, g.grade_date AS date FROM grades g 
                JOIN subjects s ON s.id = g.id_subject 
                JOIN students st ON st.id = g.id_student  
                JOIN groups_of_students gos ON gos.id_student = g.id_student 
                JOIN groups gr ON gr.id = gos.id_group 
                WHERE gos.id_group = {randint(1, 3)} AND g.id_subject = {randint(1, 5)}
                ORDER BY g.grade_date 
                LIMIT 10;""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:^5} | {row[1]:<15} | {row[2]:<30} | {row[3]:^5} | {row[4]:^10} |')

            # Report 8
            rand_group = randint(1, 3)
            rand_subject = randint(1, 5)
            print(f'\n----- Report 8 ----- grades of students in the subject groupin the last lesson')
            title = ['group', 'subject', 'student', 'grade', 'date']
            print(f'| {title[0]:^5} | {title[1]:^15} | {title[2]:^30} | {title[3]:^5} | {title[4]:^10} |')
            cur.execute(f"""SELECT gr.name AS group_name, s.name AS subject, st.name AS student, g.grade AS grade, g.grade_date AS date FROM grades g 
                JOIN subjects s ON s.id = g.id_subject 
                JOIN students st ON st.id = g.id_student  
                JOIN groups_of_students gos ON gos.id_student = g.id_student 
                JOIN groups gr ON gr.id = gos.id_group 
                WHERE gos.id_group = {rand_group} AND g.id_subject = {rand_subject} AND g.grade_date = 
                (SELECT MAX(g.grade_date) FROM grades g 
                JOIN subjects s ON s.id = g.id_subject 
                JOIN students st ON st.id = g.id_student  
                JOIN groups_of_students gos ON gos.id_student = g.id_student 
                WHERE gos.id_group = {rand_group} AND g.id_subject = {rand_subject});""")
            rows = cur.fetchall()
            for row in rows:
                # print(row)
                print(f'| {row[0]:^5} | {row[1]:<15} | {row[2]:<30} | {row[3]:^5} | {row[4]:^10} |')

            # Report 9
            print(f'\n----- Report 9 ----- a list of courses attended by the student')
            title = ['student', 'group', 'subject']
            print(f'| {title[0]:^30} | {title[1]:^5} | {title[2]:^15} |')
            cur.execute(f"""SELECT st.name AS student, g.name AS group_name, s.name AS subject FROM subjects_in_groups sig 
                JOIN groups_of_students gos ON gos.id_group = sig.id_group 
                JOIN students st ON st.id = gos.id_student 
                JOIN subjects s ON s.id = sig.id_subject 
                JOIN groups g ON g.id = sig.id_group 
                WHERE st.id = {randint(1, 30)};""")
            rows = cur.fetchall()
            for row in rows:
                print(f'| {row[0]:<30} | {row[1]:^5} | {row[2]:<15} |')

            # Report 10
            print(f'\n----- Report 10 ----- a list of courses that the teacher reads to the student')
            title = ['teacher', 'student', 'group', 'subject']
            print(f'| {title[0]:^30} | {title[1]:^30} | {title[2]:^5} | {title[3]:^15} |')
            cur.execute(f"""SELECT t.name AS teacher, st.name AS student, g.name AS group_name, s.name AS subject FROM subjects_in_groups sig 
                JOIN groups_of_students gos ON gos.id_group = sig.id_group 
                JOIN students st ON st.id = gos.id_student 
                JOIN subjects s ON s.id = sig.id_subject 
                JOIN teachers_subjects ts ON ts.id_subject = s.id
                JOIN teachers t ON t.id = ts.id_teacher 
                JOIN groups g ON g.id = sig.id_group 
                WHERE st.id = {randint(1, 30)} AND t.id = {randint(1, 3)};""")
            rows = cur.fetchall()
            for row in rows:
                print(f'| {row[0]:<30} | {row[1]:<30} | {row[2]:^5} | {row[3]:<15} |')

            # Report 11
            print(f'\n----- Report 11 ----- the average score given by the teacher to the student')
            title = ['teacher', 'student', 'av.grade']
            print(f'| {title[0]:^30} | {title[1]:^30} | {title[2]:^10} |')
            cur.execute(f"""SELECT t.name as teacher, s.name AS student, AVG(grade) AS avg_grade FROM grades g 
                JOIN teachers_subjects ts ON ts.id_subject = g.id_subject 
                JOIN teachers t ON t.id = ts.id_teacher 
                JOIN students s ON s.id = g.id_student 
                WHERE t.id = {randint(1, 3)} AND s.id = {randint(1, 30)};""")
            rows = cur.fetchall()
            for row in rows:
                print(f'| {row[0]:<30} | {row[1]:<30} | {row[2]:^10.2f} |')

            # Report 12
            rand_teacher = randint(1, 3)
            print(f'\n----- Report 12 ----- the average score given by the teacher')
            title = ['teacher', 'av.grade']
            print(f'| {title[0]:^30} | {title[1]:^10} |')
            cur.execute(f"""SELECT t.name as teacher, AVG(grade) AS avg_grade FROM grades g 
                JOIN teachers_subjects ts ON ts.id_subject = g.id_subject 
                JOIN teachers t ON t.id = ts.id_teacher 
                WHERE t.id = {randint(1, 3)};""")
            rows = cur.fetchall()
            for row in rows:
                print(f'| {row[0]:<30} | {row[1]:^10.2f} |')

            cur.close()
            print()
    else:
        print('DB not exist. Press "1 - creation of tables"\n')


