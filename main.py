import sqlite3
from datetime import datetime, timedelta
from random import randint

import faker


PATH_DB = 'homework.db'
PATH_CREATE_SQL = 'create_tables.sql'
NUMBER_STUDENTS = 50
NUMBER_TEACHERS = 5
GROUPS = ['БД-23-1', 'БД-23-2', 'БД-23-3']
DISCIPLINES = [
    'SQLite',
    'MySQL',
    'Oracle',
    'SQL Server'
    'PostgreSQL',
    'SQL Alchemy',
    'MongoDB',
    'Redis'
]


fake = faker.Faker()


def create_table(instr_file=PATH_CREATE_SQL, path_db=PATH_DB):
    with open(instr_file, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(path_db) as connection_to_db:
        cursor_db = connection_to_db.cursor()
        cursor_db.executescript(sql)
        cursor_db.close()


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = 'INSERT INTO teachers(fullname) VALUES(?);'
    curs.executemany(sql, zip(teachers,))


def seed_groups():
    sql = 'INSERT INTO groups(name) VALUES(?);'
    curs.executemany(sql, zip(GROUPS,))


def seed_disciplines():
    sql = 'INSERT INTO disciplines(name, teacher_id) VALUES(?, ?);'
    curs.executemany(sql, zip(DISCIPLINES, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES)))))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = 'INSERT INTO students(fullname, group_id) VALUES(?, ?);'
    curs.executemany(sql, zip(students, iter(randint(1, len(GROUPS)) for _ in range(len(students)))))


def seed_grades():
    sql = 'INSERT INTO grades(grade, discipline_id, student_id, date_of) VALUES(?, ?, ?, ?);'
    start_date = datetime.fromisoformat('2022-09-01')
    end_date = datetime.fromisoformat('2023-06-29')
    list_work_days = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoweekday() < 6:
            list_work_days.append(current_date)
        current_date += timedelta(days=1)
    print(len(list_work_days))
    grades = []
    for day in list_work_days:
        random_discipline = randint(1, len(DISCIPLINES))
        random_student = [randint(1, len(DISCIPLINES)) for _ in range(5)]
        for student in random_student:
            grades.append((randint(1, 12), random_discipline, student, day.date()))
    print(len(grades))
    curs.executemany(sql, grades)


if __name__ == '__main__':
    connect = sqlite3.connect(PATH_DB)
    curs = connect.cursor()
    try:
        create_table()
        seed_teachers()
        seed_disciplines()
        seed_groups()
        seed_students()
        seed_grades()
        connect.commit()
    except sqlite3.Error as err:
        print(err)
    finally:
        connect.close()
