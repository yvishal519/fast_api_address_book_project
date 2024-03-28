#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'VISHAL YADAV'
__license__ = 'This file is subject to the terms and conditions defined in file "LICENSE.txt" which is part of this source code package.'

import traceback
import pymysql
from pymysql import IntegrityError
from pymysql.constants import CLIENT

from webservices.configs import app_configurations
from webservices.utilities.logging import logger as log


class DBUtility:
    def __init__(self):
        """
        Initializer
        """
        self.db_init_flag = 0
        self.db = self.init_db()

    def init_db(self):
        """
        This function is to initialize Database
        :return db: DB connection object
        """
        try:
            db_connection = pymysql.connect(host=app_configurations.DB_HOST,
                                            user=app_configurations.DB_USER_NAME,
                                            password=app_configurations.DB_PASSWORD,
                                            db=app_configurations.DATABASE_NAME,
                                            port=int(app_configurations.DB_PORT),
                                            client_flag=CLIENT.MULTI_STATEMENTS
                                            )
            log.debug("Connection established successfully")

            self.db_init_flag = 1
            return db_connection
        except Exception as err:
            traceback.print_exc()
            log.error("Could Not Establish DB Connection - %s", err)
            raise Exception("Could Not Establish DB Connection") from err

    def close_db(self):
        """
            This function is to close connection to  Database
        :return:
        """
        if self.db_init_flag == 1:
            try:
                self.db_init_flag = 0
                self.db.close()
                del self.db
            except Exception as err:
                log.exception(str(err))
                del self.db
        else:
            log.error("DB Not Initialized before closing")

    def raw_query(self, query, auto_commit=True, tuple=None, return_id=False, single_record=False, fetch_count=False):
        """
         This method is to execute a query
        :param query:
        :param auto_commit:
        :param tuple:
        :param return_id:
        :param single_record:
        :param fetch_count:
        :return: The output of the query
        """
        if self.db_init_flag == 0:
            self.init_db()
        cursor = self.db.cursor()

        try:
            if tuple:
                cursor.execute(query, tuple)
            else:
                cursor.execute(query)
            results = []
            record_count = 0
            row_count = cursor.rowcount
            last_insert_id = cursor.lastrowid
            # Check whether there is any output for the query execution
            if cursor.rowcount > 0 and cursor.description is not None:
                if single_record:
                    results = dict((cursor.description[i][0], value) for i, value in enumerate(cursor.fetchone()))
                else:
                    results = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                               cursor.fetchall()]
                    if fetch_count and cursor.nextset():
                        record_count = cursor.fetchall()[0][0]
            else:
                log.debug("No result found for the query to fetch")

            if auto_commit:
                self.db.commit()
                cursor.close()
            log.debug("Raw query executed successfully")
            if return_id:
                return last_insert_id
            record_count = record_count if record_count else row_count
            if fetch_count:
                return results, record_count
            else:
                return results

        except IntegrityError as err:
            log.error("Error while inserting data into the table - %s", err)
            self.db.rollback()
            cursor.close()
            raise err from err

        except Exception as err:
            log.error("Error Querying tables - %s", err)
            cursor.close()
            raise Exception("Error executing the query") from err

    def execute_many(self, query, value_list):
        """
         This method is to insert multiple values into a table at a time
        :param query: Insert query
        :param value_list: list of values to be inserted into the table
        :return: True/False - query execution status
        """
        if self.db_init_flag == 0:
            self.init_db()
        cursor = self.db.cursor()

        try:
            cursor.executemany(query, value_list)
            # Check whether the query execution is successful or not
            if 0 < cursor.rowcount >= len(value_list):
                log.debug("Query executed successfully")
                self.db.commit()
                last_insert_id = cursor.lastrowid
                cursor.close()
                return True, last_insert_id
            else:
                log.error("Error executing the query - %s", query)
                self.db.rollback()
                cursor.close()
                return False, 0

        except IntegrityError as err:
            log.error("Error while inserting data into the table - %s", err)
            self.db.rollback()
            cursor.close()
            raise err from err

        except Exception as err:
            log.error("Error while inserting data into the table - %s", err)
            self.db.rollback()
            cursor.close()
            raise Exception("Error executing the query") from err
