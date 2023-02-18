import sqlite3
from datetime import datetime, timedelta
from random import randint
from pprint import pprint
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
    'SQL Server',
    'PostgreSQL',
    'SQL Alchemy',
    'MongoDB',
    'Redis'
]
QUERY_LIST = '''
Choose any action and input number:
0. Exit
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
2. Знайти студента із найвищим середнім балом з певного предмета.
3. Знайти середній бал у групах з певного предмета.
4. Знайти середній бал на потоці (по всій таблиці оцінок).
5. Знайти які курси читає певний викладач.
6. Знайти список студентів у певній групі.
7. Знайти оцінки студентів у окремій групі з певного предмета.
8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
9. Знайти список курсів, які відвідує студент.
10. Список курсів, які певному студенту читає певний викладач.
11. Середній бал, який певний викладач ставить певному студентові.
12. Оцінки студентів у певній групі з певного предмета на останньому занятті.'''
QUERY_NUM = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']


fake = faker.Faker()


def create_table(instr_file=PATH_CREATE_SQL, path_db=PATH_DB):
    with open(instr_file, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(path_db) as connection_to_db:
        cursor_db = connection_to_db.cursor()
        cursor_db.executescript(sql)
        cursor_db.close()


def seed_teachers(curs):
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = 'INSERT INTO teachers(fullname) VALUES(?);'
    curs.executemany(sql, zip(teachers,))


def seed_groups(curs):
    sql = 'INSERT INTO groups(name) VALUES(?);'
    curs.executemany(sql, zip(GROUPS,))


def seed_disciplines(curs):
    sql = 'INSERT INTO disciplines(name, teacher_id) VALUES(?, ?);'
    curs.executemany(sql, zip(DISCIPLINES, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(DISCIPLINES)))))


def seed_students(curs):
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = 'INSERT INTO students(fullname, group_id) VALUES(?, ?);'
    curs.executemany(sql, zip(students, iter(randint(1, len(GROUPS)) for _ in range(len(students)))))


def seed_grades(curs):
    sql = 'INSERT INTO grades(grade, discipline_id, student_id, date_of) VALUES(?, ?, ?, ?);'
    start_date = datetime.fromisoformat('2022-09-01')
    end_date = datetime.fromisoformat('2023-06-29')
    list_work_days = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoweekday() < 6:
            list_work_days.append(current_date)
        current_date += timedelta(days=1)
    grades = []
    for day in list_work_days:
        random_discipline = randint(1, len(DISCIPLINES))
        random_student = [randint(1, len(DISCIPLINES)) for _ in range(5)]
        for student in random_student:
            grades.append((randint(1, 12), random_discipline, student, day.date()))
    curs.executemany(sql, grades)


def create_db():
    connect = sqlite3.connect(PATH_DB)
    curs = connect.cursor()
    try:
        create_table()
        seed_teachers(curs)
        seed_disciplines(curs)
        seed_groups(curs)
        seed_students(curs)
        seed_grades(curs)
        connect.commit()
    except sqlite3.Error as err:
        print(err)
    finally:
        connect.close()


def execute_query(instr_file: str, path_db=PATH_DB):
    with open(instr_file, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(path_db) as conn:
        curs = conn.cursor()
        curs.execute(sql)
        res = curs.fetchall()
        curs.close()
        return res


if __name__ == '__main__':
    user_input = ''
    while True:
        user_input = input('Create new database?(Y/N): ')
        user_input = user_input.strip().lower()
        if user_input == 'y':
            create_db()
            print('New database created.', end='')
            break
        elif user_input == 'n':
            break
    print(QUERY_LIST)
    while True:
        user_input = input('Input action?(0-12): ')
        user_input = user_input.strip().lower()
        if user_input == '0':
            break
        if user_input in QUERY_NUM:
            try:
                str_query = f'query_{user_input}.sql'
                pprint(execute_query(str_query))
            except FileNotFoundError as e:
                print(e)
        else:
            print(f'Incorrect input: {user_input}. Try again...')
