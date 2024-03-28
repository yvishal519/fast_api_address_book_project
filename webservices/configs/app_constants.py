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

# LANGUAGE
PRIMARY_LANG = 'en'

# API Rate Limit
API_RATE_LIMIT = "5/minute"

# Monitor API Constants
LOCAL_BASE_PATH = '/tmp'
TAR_EXTENSION = '.tar.gz'
glue_log_group = '/aws-glue/jobs/output'
glue_log_stream = '{job_id}'
batch_log_group = '/aws/batch/job'

# Cloud Utility Constants
DATA_LAKE_PATH_PREFIX = "s3://"


class ApplicationModules(object):
    """
    Keys required for Modules
    """
    USER_AUTH = "User Authentication"
    ADMIN = "Admin Dashboard"
    CONFIGURE = "Configure Acquire Data"
    CONFIGURE_STAGING_DATA = "Configure -> Register Dataset"
    SCHEDULE = "Schedule Pipelines"
    MONITOR = "Monitor Pipelines"
    COMMON = "Services Used In All Screens"
    BYOD = "Bring Your Own Data"
    ANALYTICS = "Analytics"
    BULK_UPLOAD = "Bulk Upload"
    PROCESSED_DATASET = "Configure -> Create Facts & Dimension and Create Aggregates"
    DATA_CATALOG = "Data Catalog"
    CONFIGURE_PIPELINE = "Configure Pipeline Data"
    DATA_QUALITY = "Data Quality"


class ApplicationKeys:
    secure_key = "zsccfappservices"


class Tables(object):
    """
    Keys for MySQL tables
    """
    TRUCKS = 'trucks'
    DAILY_LOG = "daily_log"
    DEFECTIVE_CYLINDERS_LOG = 'defective_cylinders_log'
    LPR_LOG = 'lpr_log'


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
