import configparser
import os
from sqlalchemy import Column, String, Date, Integer, CheckConstraint

# Get the directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct path to the configuration file
config_path = os.path.join(current_dir, 'environment_variables.conf')

# Load configuration file if it exists
if os.path.exists(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
else:
    config = None
    print(f"Configuration file not found at: {config_path}")

# Define paths for data directories
data_dir = os.path.join(current_dir, 'DE_Kolkata_Test', 'templates')

# PSQL DB details from the configuration file
POSTGRES_SQL_DATABASE = config.get('PSQL_DB', 'database')
POSTGRES_SQL_USER_NAME = config.get('PSQL_DB', 'user')
POSTGRES_SQL_HOST = config.get('PSQL_DB', 'host')
POSTGRES_SQL_PORT = config.get('PSQL_DB', 'port')
POSTGRES_SQL_PASSWORD = config.get('PSQL_DB', 'password')
POSTGRES_SQL_SCHEMA = config.get('PSQL_DB', 'schema')

# template file location
parent_dir = os.path.dirname(os.path.dirname(current_dir))
template_path = os.path.join(parent_dir, 'DE_Kolkata_Test', 'templates', 'BH data.xlsx')

# table names
TBL_US_LAND_OFFSHORE_DETAILS = 'us_land_offshore_state_details'
TBL_CANADA_LAND_OFFSHORE_DETAILS = 'canada_land_offshore_province_details'

# Define columns for tables
COLUMNS_US_LAND_OFFSHORE = [
    Column('date', Date, nullable=False),
    Column('state', String(255), nullable=False),
    Column('land', Integer),
    Column('offshore', Integer),
    CheckConstraint('date IS NOT NULL AND state IS NOT NULL', name='date_state_not_null')
]

COLUMNS_CANADA_LAND_OFFSHORE = [
    Column('date', Date, nullable=False),
    Column('province', String(255), nullable=False),
    Column('land', Integer),
    Column('offshore', Integer),
    CheckConstraint('date IS NOT NULL AND province IS NOT NULL', name='date_province_not_null')
]
