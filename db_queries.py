from sqlite3 import Error, Connection
from connect import create_connection, database
from typing import List, Tuple

def get_tasks_by_user_id(conn: Connection, id: int) -> List[Tuple[str, str, int, int]]:
    cursor = conn.cursor()
    tasks = []
    try:
        cursor.execute(
            'SELECT * FROM tasks WHERE user_id = ?', (id,)
        )
        tasks = cursor.fetchall()
    except Error as e:
        print(e)
    cursor.close()
    return tasks


def get_tasks_by_status(conn: Connection, status: str) -> List[Tuple[str, str, int, int]]:
    cursor = conn.cursor()
    tasks = []
    try:
        cursor.execute('SELECT id FROM status WHERE name = ?', (status, ))
        status_id = cursor.fetchone()[0]
        cursor.execute('SELECT * FROM tasks WHERE status_id = ?', (status_id,))
        tasks = cursor.fetchall()
    except Error as e:
        print(e)
    cursor.close()
    return tasks


def apdate_status(conn: Connection, task_id: int, status: str):
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM status WHERE name = ?', (status, ))
        row = cursor.fetchone()

        if row == None:
            print(f'Status {status} not valid')
            return
        
        status_id = row[0]
        cursor.execute('UPDATE tasks SET status_id = ? WHERE id = ?', (status_id, task_id))
            
    except Error as e:
        print(e)
    conn.commit()
    cursor.close()


def find_lazy_users(conn: Connection) -> List[Tuple[str, str]]:
    cursor = conn.cursor()
    lazy_users = []
    try:
        cursor.execute('SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks)')
        lazy_users = cursor.fetchall()
    except Error as e:
        print(e)
    cursor.close()
    return lazy_users


def add_task_for_user(conn: Connection, task: Tuple[str, str], user_id: int):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)', 
                       (task[0], task[1], 1, user_id, ))
    except Error as e:
        print(e)
    conn.commit()
    cursor.close()


def get_not_completed_tasks(conn: Connection) -> List[Tuple[str, str, int, int]]:
    cursor = conn.cursor()
    nc_tasks = []

    try:
        cursor.execute('SELECT * FROM tasks WHERE NOT status_id = 3')
        nc_tasks = cursor.fetchall()
    except Error as e:
        print(e)

    cursor.close()
    return nc_tasks


def delete_task(conn: Connection, task_id: int):
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id, ))
    except Error as e:
        print(e)
    
    conn.commit()
    cursor.close()


def find_user_by_email(conn: Connection, email: str) -> str | None:
    cursor = conn.cursor()
    user = ''

    try:
        cursor.execute('SELECT fullname FROM users WHERE email LIKE ?', (f'%{email}%',))
        user = cursor.fetchone()
    except Error as e:
        print(e)
    
    cursor.close()
    return user


def update_user(conn: Connection, new_fullname: str, user_id: int):
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE users SET fullname = ? WHERE id = ?', (new_fullname, user_id))
    except Error as e:
        print(e)
    
    conn.commit()
    cursor.close()


def count_tasks_by_status(conn: Connection):
    tasks_status = None
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT status_id, COUNT (title) FROM tasks GROUP BY status_id') 
        tasks_status = cursor.fetchall()
    except Error as e:
        print(e)

    return tasks_status


def select_tasks_by_domen(conn: Connection, domen: str) -> List[Tuple[str, str]]:
    domen_tasks = []
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT t.title, t.description \
                       FROM tasks AS t \
                       JOIN users AS u ON u.id = t.user_id \
                       WHERE u.email LIKE ?', (f'%{domen}%',))
        domen_tasks = cursor.fetchall()
        print(domen_tasks)
    except Error as e:
        print(e)
    
    cursor.close()



    return domen_tasks


def select_tasks_without_description(conn: Connection) -> List[str]:
    tasks_without_description = []
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT title \
                       FROM tasks\
                       WHERE description IS NULL OR description = ""')
        tasks_without_description = [t[0] for t in cursor.fetchall()]
    except Error as e:
        print(e)
    
    cursor.close()
    return(tasks_without_description)


def select_users_tasks_by_status(conn: Connection, status: str):
    users_tasks = []
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id FROM status WHERE name = ?', (status, ))
        status_id = cursor.fetchone()
        print(status_id)
        cursor.execute('SELECT u.fullname, t.title, t.status_id\
                       FROM users AS u\
                       INNER JOIN tasks AS t\
                       ON t.user_id = u.id\
                       WHERE t.status_id = ?',
                       (status_id[0],))
        users_tasks = cursor.fetchall()
    except Error as e:
        print(e)
    
    cursor.close()
    return users_tasks


def get_users_count_tasks(conn: Connection) -> List[Tuple[str, int]]:
    cursor = conn.cursor()
    users_count_tasks = []

    try:
        cursor.execute('SELECT\
                        u.fullname AS username, \
                        COUNT (t.id) AS total_tasks\
                       FROM users AS u\
                       LEFT JOIN tasks AS t\
                       ON u.id = t.user_id\
                       GROUP BY u.id, u.fullname\
                       ')

        users_count_tasks = cursor.fetchall()
    except Error as e:
        print(e)
    
    cursor.close()
    return users_count_tasks


    
if __name__ == '__main__':
    with create_connection(database) as conn:
        print(get_tasks_by_user_id(conn, 5)) # отримання завдань конкретного користувача за його user_id
        print(get_tasks_by_status(conn, 'new')) # вибор завдань з конкретним статусом, наприклад, 'new'
        apdate_status(conn, 4, 'in progress') # Зміна статусу конкретного завдання на інший статус ("new", "in progress", "completed")
        print(find_lazy_users(conn)) # Отримати список користувачів, які не мають жодного завдання
        add_task_for_user(conn, ('new task', 'new description. second sentence.'), 2) # Додати нове завдання для конкретного користувача
        print(get_not_completed_tasks(conn)) # Отримати всі завдання, які ще не завершено
        delete_task(conn, 10) # Видалити конкретне завдання. 
        print(find_user_by_email(conn, 'fhunter@example.net')) # Знайти користувачів з певною електронною поштою
        update_user(conn, 'peter parker', 5) # Оновити ім'я користувача
        print(count_tasks_by_status(conn)) # Отримати кількість завдань для кожного статусу. 
        print(select_tasks_by_domen(conn, '@example.net')) # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
        print(select_tasks_without_description(conn)) # Отримати список завдань, що не мають опису
        print(select_users_tasks_by_status(conn, 'in progress')) # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
        print(get_users_count_tasks(conn))

