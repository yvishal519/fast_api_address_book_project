#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Vishal Yadav'

import configparser

config = configparser.ConfigParser()
config.read('configurations/environment_variables.conf')

# API-Service calling URL
api_service_url = "/backend"

SERVICE_HOST = config["SERVICE"]["host"]
SERVICES_PORT = int(config.get('SERVICE', 'port'))
ENVIRONMENT = config['SERVICE']['environment']

# Getting details from the configuration file for the Logger
LOG_FILE_NAME = config.get('LOG', 'log_file_name')
FILE_LOG_ENABLED = config.get('LOG', 'file_logging_enabled')
CONSOLE_LOG_ENABLED = config.get('LOG', 'console_logging_enabled')

# Getting details from the configuration file for the SQLite DB
MAX_CONNECTION = config.get('SQLite_DB', 'max_connections')
DB_FILE = config.get('SQLite_DB', 'db_file')



