from sqlite3 import Error
from connect import create_connection, database


def truncate_table(conn, table_name):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
    except Error as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()


if __name__ == "__main__":

    tables = ["users", "status", "tasks"]
    with create_connection(database) as conn:
        for table in tables:
            truncate_table(conn, table)
