from typing import List

from fastapi import HTTPException, status
from webservices.microservices.model.model import Address, AddressOut, AddressListOut
from webservices.utilities.logger_utils import logger
from webservices.utilities.sql_lite_dbutils import ConnectionPool, create_tables_if_not_exist


class AddressHandler:
    """
    Handles CRUD operations for addresses in the database.
    """

    def __init__(self, db_file, max_connections=5):
        """
        Initializes the AddressHandler with the specified database file and maximum connections.
        """
        self.db_file = db_file
        self.connection_pool = ConnectionPool(max_connections)
        create_tables_if_not_exist(db_file)

    def _execute_query(self, query, params=None, fetchone=False, fetchall=False):
        """
        Executes the specified SQL query with optional parameters and fetch options.
        """
        conn = self.connection_pool.get_connection(self.db_file)
        try:
            c = conn.cursor()
            if params:
                c.execute(query, params)
            else:
                c.execute(query)

            if fetchone:
                result = c.fetchone()
            elif fetchall:
                result = c.fetchall()
            else:
                result = None

            conn.commit()
            return result
        except Exception as err:
            logger.exception(f"Error occurred while executing query: {query}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
        finally:
            self.connection_pool.release_connection(conn)

    def create_address(self, request_body: Address):
        """
        Creates a new address in the database.
        """
        query = "INSERT INTO addresses (street_address, city, state, postal_code, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)"
        params = (request_body.street_address, request_body.city, request_body.state, request_body.postal_code,
                  request_body.latitude, request_body.longitude)
        address_id = self._execute_query(query, params)
        if not address_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to create the address")
        return {**request_body.dict(), "id": address_id}

    def update_address(self, address_id: int, request_body: Address):
        """
        Updates an existing address in the database.
        """
        query = "UPDATE addresses SET street_address=?, city=?, state=?, postal_code=?, latitude=?, longitude=? WHERE id=?"
        params = (request_body.street_address, request_body.city, request_body.state, request_body.postal_code,
                  request_body.latitude, request_body.longitude, address_id)
        result = self._execute_query(query, params)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return {**request_body.dict(), "id": address_id}

    def delete_address(self, address_id: int):
        """
        Deletes an address from the database.
        """
        query = "DELETE FROM addresses WHERE id=?"
        result = self._execute_query(query, (address_id,))
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
        return {"message": "Address deleted successfully"}

    def get_addresses_within_distance(self, latitude: float, longitude: float, distance: float) -> List[AddressOut]:
        """
        Retrieve addresses within a given distance and location coordinates.
        """
        addresses = []
        query = "SELECT * FROM addresses"
        rows = self._execute_query(query, fetchall=True)
        user_location = (latitude, longitude)
        for row in rows:
            address_location = (row[5], row[6])  # latitude and longitude
            if distance.distance(user_location, address_location).miles <= distance:
                addresses.append({
                    "id": row[0],
                    "street_address": row[1],
                    "city": row[2],
                    "state": row[3],
                    "postal_code": row[4],
                    "latitude": row[5],
                    "longitude": row[6]
                })
        return addresses
