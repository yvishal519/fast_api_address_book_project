
# Baker Hughes (BH) Data Extractor

Develop PostgreSQL schema and tables to store data from Baker Hughes' weekly rig report. Create ETL process in Python to extract, transform, and load data from provided Excel file into the designed SQL tables. Deliverables include SQL schema/table creation script and Python ETL code for data processing and loading.
## Prerequisites

- Python 3.10 is required for running this project.
- PostgreSQL database details are needed for database operations.
- An existing Excel template file with the specified naming convention is required
## Installation
1. Navigate to required path using cd command

    `cd \DE_Kolkata_Test\requirements`
2. Install required packages using pip

    `pip install -r requirements.txt`

### Directory Structure
    DE_Kolkata_Test
        ├── configs
        │     └── environment_variables.conf
        ├── requirements
        │      └── requirements.txt
        ├── src        
        │   └── baker_hughes_extractor
        │       ├── main.py
        │       ├── utils
        │             ├── helper.py
        │             └── db_utils.py
        ├── templates 
        │     └── BH data.xlsx
        ├── Dockerfile

        


## Database Details
Ensure to provide the following PostgreSQL database details to environment_variable.conf

`database` = psql_database_name

`user` = user_name

`password` = password

`port` = port

`host` = host_details

`schema` = web_scrapes (default)

## Usage
1. Navigate to the location of main.py in the project directory
    `cd \DE_Kolkata_Test`

2. Run main.py using Python
    `python main.py`

# Input and Output Definitions for the Provided Code
## Input :
### 1. Excel Data Sheets:
* The code expects Excel sheets containing data for Canada and the US split by province/state.
* The data should be structured with specific headers for each state/province.
### 2. Database Configuration:
* PostgreSQL database connection details such as host, port, username, password, and database name are required.
* Schema names and table names are defined for storing the extracted data.
### 3. Python Environment:
* The code relies on specific Python packages and libraries like pandas, sqlalchemy, and standard libraries such as logging and sys
## Output :
### 1. Data Transformation:
* The code orchestrates data extraction, transformation, and loading into a PostgreSQL database.
* Extracted data is transformed based on predefined headers for each state/province.
### 2. Database Operations:
* Schema creation: The code creates a schema in the database.
* Table creation: Tables are created in the specified schema with predefined columns.
* Data Loading: Extracted data is saved to PostgreSQL tables using specified save types ('append', 'replace', 'fail').
### 3. Logging Information:
* The code logs information about the execution process, errors encountered, and successful operations.
* Logging is configured to display timestamps, log levels, and messages to the console.
## Functionality:
* The main() function orchestrates the entire process of schema creation, table creation, data extraction, transformation, and loading into PostgreSQL for both Canada and the US data.
* Data is extracted from Excel sheets based on predefined headers for each state/province and saved to the respective tables in the database.
## Note:
* Ensure that the Excel sheets are structured according to the expected headers for each state/province.
* Configure the PostgreSQL database connection details and schema/table names appropriately before running the code.
> By following the input requirements and understanding the expected output, you can effectively utilize the provided code for data extraction, transformation, and loading operations into a PostgreSQL database

## Author
[yvishal518@gmail.com](mailto:yvishal518@gmail.com)

[<img src="https://norakramerdesigns.b-cdn.net/wp-content/uploads/2015/04/linedin-profile-button.jpg" width="100">](https://www.linkedin.com/in/yvishal519)

#   f a s t _ a p i _ a d d r e s s _ b o o k _ p r o j e c t  
 