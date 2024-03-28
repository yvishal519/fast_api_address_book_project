#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Vishal Yadav'
__license__ = 'This file is subject to the terms and conditions defined in file "LICENSE.txt" ' \
              'which is part of this source code package.'

import configparser
import os

config = configparser.ConfigParser()
config.read('configurations/environment_variables.conf')

# API-Service calling URL
api_service_url = "/backend"

SERVICE_HOST = config["SERVICE"]["host"]
SERVICES_PORT = int(config.get('SERVICE', 'port'))
ENVIRONMENT = config['SERVICE']['environment']
API_RATE_LIMIT = config['SERVICE']['api_rate_limit']
COOKIE_MAX_AGE = int(config['SERVICE']['cookie_max_age'])

# Getting details from the configuration file for the Logger
LOG_FILE_NAME = config.get('LOG', 'log_file_name')
FILE_LOG_ENABLED = config.get('LOG', 'file_logging_enabled')
CONSOLE_LOG_ENABLED = config.get('LOG', 'console_logging_enabled')

# MYSQL DB details
DATABASE_NAME = config.get('MYSQL_DB', 'database')
DB_USER_NAME = config.get('MYSQL_DB', 'user')
DB_HOST = config.get('MYSQL_DB', 'host')
DB_PORT = config.get('MYSQL_DB', 'port')
DB_PASSWORD = config.get('MYSQL_DB', 'password')

# PSQL DB details
POSTGRES_SQL_DATABASE = config.get('PSQL_DB', 'database')
POSTGRES_SQL_USER_NAME = config.get('PSQL_DB', 'user')
POSTGRES_SQL_HOST = config.get('PSQL_DB', 'host')
POSTGRES_SQL_PORT = config.get('PSQL_DB', 'port')
POSTGRES_SQL_PASSWORD = config.get('PSQL_DB', 'password')
POSTGRES_SQL_SCHEMA = config.get('PSQL_DB', 'schema')


#################################
# PATHS
#################################
CONFIG_PATH = "webservices/configs"
HOME_PATH = os.getcwd()


