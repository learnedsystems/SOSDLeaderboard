import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"./indexes.db"

    sql_create_indexes_table = """ CREATE TABLE IF NOT EXISTS indexes (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        variant integer NOT NULL,
                                        latency real NOT NULL,
                                        size integer NOT NULL,
                                        build_time integer NOT NULL,
                                        searcher text NOT NULL,
                                        dataset text NOT NULL
                                    ); """

    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_indexes_table)
    else:
        print("Error! Database connection failed.")


if __name__ == '__main__':
    main()