from sqlite3 import Error, Connection
from connect import create_connection, database


def drop_table(conn: Connection, table_name: str):
    
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE {table_name}")
    except Error as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()


if __name__ == "__main__":

    tables = ["users", "status", "tasks"]
    with create_connection(database) as conn:
        for table in tables:
            drop_table(conn, table)