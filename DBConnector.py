import mysql.connector.pooling


# Singleton pattern decorator
def singleton(cls, *args, **kw):
    instance = {}

    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


# Get database connection pool
@singleton
class _DBConnector:

    def __init__(self):
        cnf = {
            'user': 'root',
            'password': 'zhou',
            'host': 'localhost',
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'pool_name': 'my_pool',
            'pool_size': 3
        }
        self.__cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**cnf)

    def get_cnx_pool(self):
        return self.__cnx_pool


# Create a cursor in a connection
class GetCursor:

    def __enter__(self):
        self.__cnx = _DBConnector().get_cnx_pool().get_connection()
        self.__cur = self.__cnx.cursor()
        return self.__cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.__cnx.commit()
        else:
            self.__cnx.rollback()
        self.__cur.close()
        self.__cnx.close()