__author__ = 'Vishal Yadav'
__license__ = 'This file is subject to the terms and conditions defined in file "LICENSE.txt" which is part of this source code package.'

# Methods
GET = "GET"
POST = "POST"

# Error message configs
METHOD_NOT_SUPPORTED = "Method not supported!"

SUCCESS_STATUS = "SUCCESS"
FAILED_STATUS = "FAILED"
ERROR = "ERROR"
RESULT = "RESULT"
STATUS = "STATUS"


class ApplicationModules(object):
    """
    Keys required for Modules
    """
    USER_AUTH = "User Authentication"


class Tables(object):
    """
    Keys for MySQL tables
    """
    ADDRESSES_TBL = 'addresses'


def result_success_template(data, message="Success", status=SUCCESS_STATUS):
    return {
        "status": status,
        "message": message,
        "data": data
    }


def result_error_template(message=None, data=None):
    if message:
        return {
            "status": FAILED_STATUS,
            "message": message,
            "data": data,
        }
    else:
        return {
            "status": FAILED_STATUS,
            "message": "Error while processing the request",
            "data": data,

        }


CREATE_TBL_QUERY = '''CREATE TABLE IF NOT EXISTS {table_name}
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     street_address TEXT,
                     city TEXT,
                     state TEXT,
                     postal_code TEXT,
                     latitude REAL,
                     longitude REAL)'''
