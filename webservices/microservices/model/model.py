from pydantic import BaseModel
from typing import List


# Address model for input validation
class Address(BaseModel):
    street_address: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float


# Address model for output validation
class AddressOut(BaseModel):
    id: int
    street_address: str
    city: str
    state: str
    postal_code: str
    latitude: float
    longitude: float


class AddressListOut(BaseModel):
    data: List[AddressOut]


class LocationParams(BaseModel):
    latitude: float
    longitude: float
    distance: float
