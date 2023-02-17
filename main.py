import sqlite3
from datetime import date, datetime, timedelta
from random import randint
from contextlib import contextmanager

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
connect = sqlite3.connect(PATH_DB)
curs = connect.cursor()

@contextmanager
def connection(path_db=PATH_DB):
    conn = None
    try:
        conn = sqlite3.connect(path_db)
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()


def create_table(instr_file=PATH_CREATE_SQL, path_db=PATH_DB):
    with open(instr_file, 'r') as fd:
        sql = fd.read()
    with sqlite3.connect(path_db) as connection_to_db:
        cursor_db = connection_to_db.cursor()
        cursor_db.executescript(sql)
        cursor_db.close()


def seed_teachers(number=NUMBER_TEACHERS):
    teachers = [fake.name() for _ in range(number)]
    sql = 'INSERT INTO teachers(fullname) VALUES(?);'
    curs.executemany(sql, zip(teachers,))


def seed_disciplines(disc=DISCIPLINES):
    sql = 'INSERT INTO disciplines(name), teachers_id VALUES(?);'
    teachers = [fake.name() for _ in range(number)]
    curs.executemany(sql, zip(teachers,))





if __name__ == '__main__':
    create_table()
