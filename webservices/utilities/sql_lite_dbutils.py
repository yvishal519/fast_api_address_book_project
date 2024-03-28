import sqlite3
import threading
from queue import Queue


class ConnectionPool:
    def __init__(self, max_connections):
        self._max_connections = max_connections
        self._lock = threading.Lock()
        self._pool = Queue(maxsize=max_connections)

    def get_connection(self, db_file):
        with self._lock:
            if self._pool.empty() and self._pool.qsize() < self._max_connections:
                conn = sqlite3.connect(db_file)
                return conn
            else:
                return self._pool.get()

    def release_connection(self, conn):
        with self._lock:
            if self._pool.qsize() < self._max_connections:
                self._pool.put(conn)
            else:
                conn.close()


def create_tables_if_not_exist(db_file):
    conn = sqlite3.connect(db_file)
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS addresses
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     street_address TEXT,
                     city TEXT,
                     state TEXT,
                     postal_code TEXT,
                     latitude REAL,
                     longitude REAL)''')
        conn.commit()
    except Exception as e:
        print("Error occurred while creating tables")
        raise
    finally:
        conn.close()
