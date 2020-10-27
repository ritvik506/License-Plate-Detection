import sqlite3
import datetime

connect = sqlite3.connect('num_plate.db')
cur = connect.cursor()


def init_database():
    try:
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS num_plate (num_plate TEXT NOT NULL PRIMARY KEY, time_enter TEXT)''')
        connect.commit()
        print('Connected to database')
    except:
        print("error could not load database")
        connect.rollback()


# Insert into the database
def insert_into_database(numplate):
    cur.execute('''INSERT OR IGNORE INTO num_plate (num_plate, time_enter) VALUES (?, ?)''', (numplate, datetime.datetime.now()))
    print('Inserted Values.')
    connect.commit()
