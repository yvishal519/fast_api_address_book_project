from fastapi import APIRouter, HTTPException
from starlette import status
from webservices.utilities.logger_utils import logger
from webservices.microservices.model.model import Address, AddressOut, AddressListOut, LocationParams
from webservices.microservices.handler.handler import AddressHandler
from webservices.utilities.sql_lite_dbutils import ConnectionPool

# Create an instance of AddressHandler for reuse
address_handler = AddressHandler(db_file='address_book.db')
connection_pool = ConnectionPool(max_connections=5)  # Create a connection pool

address_router = APIRouter()


# Endpoint to create a new address
@address_router.post("/addresses/", response_model=AddressOut)
def create_address_api(request_body: Address):
    """
    Create a new address.
    """
    try:
        result = address_handler.create_address(request_body)
        return result
    except Exception as err:
        logger.exception("Error occurred while creating an address")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Endpoint to update an existing address
@address_router.put("/addresses/{address_id}", response_model=AddressOut)
def update_address_api(address_id: int, request_body: Address):
    """
    Update an existing address.
    """
    try:
        result = address_handler.update_address(address_id, request_body)
        return result
    except Exception as err:
        logger.exception("Error occurred while updating the address")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


# Endpoint to delete an address
@address_router.delete("/addresses/{address_id}")
def delete_address_api(address_id: int):
    """
    Delete an address.
    """
    try:
        result = address_handler.delete_address(address_id)
        return result
    except Exception as err:
        logger.exception("Error occurred while deleting the address")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@address_router.post("/distance/", response_model=AddressListOut)
def get_addresses_within_distance_api(location_params: LocationParams):
    """
    Retrieve addresses within a given distance and location coordinates.
    """
    try:
        result = address_handler.get_addresses_within_distance(location_params.latitude, location_params.longitude, location_params.distance)
        return {"__root__": result}
    except Exception as err:
        logger.exception("Error occurred while retrieving addresses within distance")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")