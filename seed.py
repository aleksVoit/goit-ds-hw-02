from sqlite3 import Error, Connection
from faker import Faker
from random import randint
from connect import create_connection, database

fake = Faker()
USERS_NUMBER = 10
STATUSES = [("new", ), ("in progress", ), ("completed", )]
TASKS_NUMBER = 30

def gen_users(n: int) -> list[tuple[str, str]]:
    users: list[tuple[str, str]] = []
    for _ in range(n):
        fullname = fake.name()
        email = fake.email()
        users.append((fullname, email))
    return users


def add_users(conn: Connection,
               users: list[tuple[str, str]]):
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO users (fullname, email) VALUES (?, ?)", users)
    conn.commit()
    cursor.close()


def add_status(conn: Connection,
                statuses: list[tuple[str]]):
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO status (name) VALUES (?)", statuses)
    conn.commit()
    cursor.close()


def gen_tasks(n: int) -> list[tuple[str, str]]:
    tasks: list[tuple[str, str]] = []
    for _ in range(n):
        title = fake.sentence(nb_words=4)
        description = fake.paragraph(nb_sentences=4)
        tasks.append((title, description))
    return tasks


# def add_tasks(conn: Connection,
#                 tasks: list[tuple[str, str]],
#                 users: list[tuple[str, str]],
#                 statuses: list[tuple[str]]):

#     cursor = conn.cursor()

#     for user in users:
#         user_id: int | None = None
#         try:
#             cursor.execute("SELECT id FROM users WHERE fullname = ?", (user[0],))
#             user_id = cursor.fetchone()[0]
#             print(user_id)

#         except sqlite3.Error as e:
#             print(e)

#         for task in tasks:
#             print(task)

#             status_id = randint(1, len(statuses))
#             try:
#                 cursor.execute(
#                     "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
#                     (task[0], task[1], status_id, user_id),
#                 )
#             except Error as e:
#                 print(e)

#     conn.commit()
#     cursor.close()


def add_tasks(conn: Connection,
              tasks: list[tuple[str, str]]):
    
    cursor = conn.cursor()
    for task in tasks:
        try:
            cursor.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)',
                           (task[0],
                            task[1],
                            randint(1, len(STATUSES)),
                            randint(1, USERS_NUMBER)))
        except Error as e:
            print(e)
    
    conn.commit()
    cursor.close()


if __name__ == "__main__":
    with create_connection(database) as conn:
        users = gen_users(USERS_NUMBER)
        #statuses: list[tuple[str]] = [("new", ), ("in progress", ), ("completed", )]
        tasks = gen_tasks(TASKS_NUMBER)
        add_users(conn, users)
        add_status(conn, STATUSES)
        add_tasks(conn, tasks)
