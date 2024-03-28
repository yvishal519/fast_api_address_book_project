import psycopg2
from webservices.utilities.logging import logger


class PSQLDBUtils:
    def __init__(self, dbname, port, schema, user, password, host):
        self.dbname = dbname
        self.port = port
        self.schema = schema
        self.user = user
        self.password = password
        self.host = host
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            logger.debug("PostgreSQL connection created for Host: " + self.host + ", Port: "
                         + str(self.port) + ", Username: " + self.user + ", Password: *******, Database: " + self.dbname)
        except psycopg2.Error as e:
            logger.error("Error connecting to the database: %s", str(e))
            raise e

    def insert(self, table_name, data):
        try:
            with self.conn.cursor() as cursor:
                # Construct and execute the insert query using parameterized query
                columns = ', '.join(data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                query = f"INSERT INTO {self.schema}.{table_name} ({columns}) VALUES ({placeholders})"
                # logger.debug(f"Data insert Query to {table_name} is ", query)

                cursor.execute(query, list(data.values()))
                self.conn.commit()
            logger.info(f"Data inserted into {table_name} table successfully")
        except psycopg2.Error as e:
            logger.error(f"Error inserting data into {table_name} table: {str(e)}")
            raise e

    def update(self, table, set_values, condition):
        try:
            with self.conn.cursor() as cursor:
                # Construct and execute the update query using parameterized query
                query = f"UPDATE {self.schema}.{table} SET {', '.join([f'{col}=%s' for col in set_values.keys()])} WHERE {condition}"
                cursor.execute(query, list(set_values.values()))
                self.conn.commit()
            logger.info("Data updated successfully")
        except psycopg2.Error as e:
            logger.error("Error updating data: %s", str(e))
            raise e

    def execute_query(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                # Execute the query with optional parameters
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                rows = cursor.fetchall()
                result = []
                if rows or rows is not None:
                    for row in rows:
                        result.append(row)
                else:
                    logger.error("No Data Found")
            logger.info("Query executed successfully")
            return result
        except psycopg2.Error as e:
            logger.error("Error executing the query: %s", str(e))
            raise e

    def delete(self, table, condition):
        try:
            with self.conn.cursor() as cursor:
                # Construct and execute the delete query
                query = f"DELETE FROM {self.schema}.{table} WHERE {condition}"
                cursor.execute(query)
                self.conn.commit()
            logger.info("Data deleted successfully")
        except psycopg2.Error as e:
            logger.error("Error deleting data: %s", str(e))

    def fetch_one(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                # Execute the query with optional parameters
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                row = cursor.fetchone()
            logger.info("Fetched one row successfully")
            return row
        except psycopg2.Error as e:
            logger.error("Error fetching one row: %s", str(e))
            raise e

    def close(self):
        try:
            if self.conn is not None:
                self.conn.close()
                logger.warning("Connection to the database closed")
        except psycopg2.Error as e:
            logger.error("Error closing the database connection: %s", str(e))
            raise e

