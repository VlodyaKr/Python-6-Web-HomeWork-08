import sqlite3 as sql

SQL_CREATE_TABLES = """CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHARE(30) NOT NULL);
    CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHARE(30) NOT NULL);
    CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHARE(15) NOT NULL);
    CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHARE(5) NOT NULL);
    CREATE TABLE IF NOT EXISTS groups_of_students (
    id_group INTEGER NOT NULL,
    id_student INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS teachers_subjects (
    id_teacher INTEGER NOT NULL,
    id_subject INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS subjects_in_groups (
    id_group INTEGER NOT NULL,
    id_subject INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    id_student INTEGER,
    id_subject INTEGER,
    grade INTEGER,
    grade_date DATE);"""

def create_tables():
    with sql.connect('univer.db') as conn:
        cur = conn.cursor()
        cur.executescript(SQL_CREATE_TABLES)
        cur.close()
        print('DB is created\n')