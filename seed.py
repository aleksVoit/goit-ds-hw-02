from sqlite3 import Error
from faker import Faker
from random import randint
from connect import create_connection, database

fake = Faker()


def gen_users(n: int) -> list[tuple[str,str]]:
    users = []
    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        users.append((fullname, email))
    return users


def add_users(conn, users: list[tuple[str,str]]):
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO users (fullname, email) VALUES (?, ?)',
        users
    )
    conn.commit()
    cursor.close()


def add_status(conn, statuses):
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO status (name) VALUES (?)',
        statuses
    )
    conn.commit()
    cursor.close()


def gen_tasks(n: int) -> list[tuple[str, str]]:
    tasks = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=4)
        tasks.append((title, description))
    return tasks


def add_tasks(conn, tasks: list, users: list, statuses: list):

    cursor = conn.cursor()

    for user in users:
        
        try:
            cursor.execute('SELECT id FROM users WHERE fullname = ?', (user[0],))
            user_id = cursor.fetchone()

        except Error as e:
            print(e)
    
        for task in tasks:
            print(task)
            
            status_id = randint(1, len(statuses))
            try:
                cursor.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)',
                                (task[0], task[1], status_id, user_id[0] ))
            except Error as e:
                print(e)
    
    conn.commit()
    cursor.close()



if __name__ == '__main__':
    with create_connection(database) as conn:
        users = gen_users(10)
        statuses = [('new', ), ('in progress', ), ('completed', )]
        tasks = gen_tasks(10)
        add_users(conn, users)
        add_status(conn, statuses)
        add_tasks(conn, tasks, users, statuses)