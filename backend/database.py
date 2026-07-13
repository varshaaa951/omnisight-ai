from psycopg2 import pool

connection_pool = pool.SimpleConnectionPool(
    1,
    10,
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

def get_connection():
    return connection_pool.getconn()

def return_connection(conn):
    connection_pool.putconn(conn)