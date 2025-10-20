from sqlite3 import Error, Connection
from connect import create_connection, database


def create_table(conn: Connection, cr_table_sql: str):
    try:
        cursor = conn.cursor()
        cursor.execute(cr_table_sql)
        conn.commit()
    except Error as e:
        print(e)


if __name__ == "__main__":
    sql_create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
        );
        """

    sql_create_status_table = """
        CREATE TABLE IF NOT EXISTS status (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) UNIQUE
        );
        """

    sql_create_tasks_table = """
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER,
        user_id INTEGER,
        FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

    with create_connection(database) as conn:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_status_table)
        create_table(conn, sql_create_tasks_table)
