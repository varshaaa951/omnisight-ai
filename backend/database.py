from psycopg2 import pool

# Create a connection pool for the OmniSight database
omnisight_pool = pool.SimpleConnectionPool(
    1,
    10,
    host="localhost",
    database="omnisight",
    user="admin",
    password="admin123"
)

# Create a connection pool for the Marketing database
marketing_pool = pool.SimpleConnectionPool(
    1,
    10,
    host="localhost",
    database="marketing_db",
    user="admin",
    password="admin123"
)


def get_connection(database_name="omnisight"):
    if database_name == "marketing_db":
        return marketing_pool.getconn()
    return omnisight_pool.getconn()


def return_connection(conn, database_name="omnisight"):
    if database_name == "marketing_db":
        marketing_pool.putconn(conn)
    else:
        omnisight_pool.putconn(conn)