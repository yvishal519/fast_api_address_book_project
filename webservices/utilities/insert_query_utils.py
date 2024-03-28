from webservices.utilities.logging import logger
from webservices.utilities.psql_db_utils import PSQLDBUtils
from webservices.configs import app_configurations as app_config
from webservices.configs.app_constants import Tables


class DataBaseOperations:
    def __enter__(self):
        self.db_utils = PSQLDBUtils(
            dbname=app_config.POSTGRES_SQL_DATABASE,
            port=app_config.POSTGRES_SQL_PORT,
            schema=app_config.POSTGRES_SQL_SCHEMA,
            user=app_config.POSTGRES_SQL_USER_NAME,
            password=app_config.POSTGRES_SQL_PASSWORD,
            host=app_config.POSTGRES_SQL_HOST
        )
        self.db_utils.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.db_utils.close()

    def _insert_data(self, table_name, data, success_message):
        try:
            self.db_utils.insert(table_name=table_name, data=data)
            logger.info(success_message)
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {str(e)}")

    def insert_truck_data(self, license_plate_number):
        self._insert_data(
            table_name=Tables.TRUCKS,
            data={"license_plate_number": license_plate_number},
            success_message="Truck data inserted successfully"
        )

    def insert_daily_log(self, truck_id, total_cylinders_count, defective_cylinders_count):
        self._insert_data(
            table_name=Tables.DAILY_LOG,
            data={
                "truck_id": truck_id,
                "total_cylinders_count": total_cylinders_count,
                "defective_cylinders_count": defective_cylinders_count
            },
            success_message="Daily log data inserted successfully"
        )

    def insert_lpr_log(self, truck_id, image_path):
        self._insert_data(
            table_name=Tables.LPR_LOG,
            data={"truck_id": truck_id, "image_path": image_path},
            success_message="LPR log data inserted successfully"
        )

    def insert_defective_cylinders_log(self, truck_id, image_path):
        self._insert_data(
            table_name=Tables.DEFECTIVE_CYLINDERS_LOG,
            data={"truck_id": truck_id, "image_path": image_path},
            success_message="Defective cylinders log data inserted successfully"
        )


# Usage example:
with DataBaseOperations() as db_operations:
    db_operations.insert_truck_data(1111345)
    db_operations.insert_daily_log(1, 1020, 25)
    db_operations.insert_lpr_log(1, "path/to/image.jpg")
    db_operations.insert_defective_cylinders_log(1, "path/to/image.jpg")
