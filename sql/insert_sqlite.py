import csv
import sqlite3
import os

from sqlite3 import Error
from statistics import median

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def insert_index_file(conn, index_entry):
    """
    Insert a new index benchmark result into the index table
    :param conn:
    :param index:
    :return: index id
    """
    sql = ''' INSERT OR IGNORE INTO indexes(name,variant,latency,size,build_time,searcher,dataset)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, index_entry)
    conn.commit()
    return cur.lastrowid

def get_all_indexes(conn):
    """
    Return every index in the index benchmark results database
    """
    sql = ''' SELECT * FROM indexes '''
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    return rows

def get_index_results(conn, index):
    """
    Return all entries associated with the specified index 
    """
    sql = f''' SELECT * FROM indexes WHERE name=? '''
    cur = conn.cursor()
    cur.execute(sql, (index,))

    rows = cur.fetchall()
    return rows

def delete_index_results(conn, index):
    """
    Remove all entries associated with specified index name
    (in the event that a benchmarked index needs to be completely updated)
    """
    sql = f''' DELETE FROM indexes
               WHERE name=? '''
    cur = conn.cursor()
    cur.execute(sql, (index,))
    conn.commit()

def process_csv(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            rows.append(row)

    return rows

def read_csv_into_sqlite(conn, filename):
    rows = process_csv(filename)
    for row in rows:
        insert_index_file(conn, row)

if __name__ == "__main__":
    conn = create_connection("./indexes.db")

    data_dir = './benchmark_results/'
    csvfiles = os.listdir(data_dir)

    for file in csvfiles:
        read_csv_into_sqlite(conn, data_dir + file)
