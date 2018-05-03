import mysql.connector
import mysql.connector.errors


# Singleton pattern decorator
def singleton(cls, *args, **kw):
    instance = {}

    def _singleton():
        if cls not in instance:
            instance[cls] = cls(*args, **kw)
        return instance[cls]

    return _singleton


# Get a database connection
@singleton
class _DBConnector:

    def __init__(self):
        user = 'root'
        password = 'zhou'
        host = 'localhost'
        self.__cnx = mysql.connector.connect(user=user, password=password, host=host)
        self.__set_utf8mb4()

    def __del__(self):
        if hasattr(self, '__cnx'):
            self.__cnx.close()

    def __set_utf8mb4(self):
        cur = self.__cnx.cursor(buffered=True)
        cur.execute('SET NAMES utf8mb4')
        self.__cnx.commit()
        cur.close()

    def get_cnx(self):
        return self.__cnx


# Create a cursor
class GetCursor:

    def __enter__(self):
        self.__cnx = _DBConnector().get_cnx()
        self.__cur = self.__cnx.cursor()
        return self.__cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            self.__cnx.commit()
        else:
            self.__cnx.rollback()
        self.__cur.close()
