import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def add_to_channel(conn, sql, value):
    """
        Create a new task
        :param conn:
        :param sql:
        :param value:
        :return:
        """
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()

    return cur.lastrowid


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return error: boolean
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        return True
    except Error as e:
        print(e)
        return False


def update(conn, sql, value):
    """
        Create a new task
        :param conn:
        :param sql:
        :param value:
        :return:
        """
    cur = conn.cursor()
    cur.execute(sql, value)
    conn.commit()

    return cur.lastrowid


def select(conn, sql):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :param sql: string
    :return results: list
    """
    result =[]
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()

    for row in rows:
        result.append(row)
    return result
