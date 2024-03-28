from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from webservices.utilities.logger_utils import logger

# Define the APIRouter
address_router = APIRouter()


# Define the Pydantic model for input validation
class Coordinates(BaseModel):
    latitude: float = Field(..., description="The latitude of the address")
    longitude: float = Field(..., description="The longitude of the address")


class Address(BaseModel):
    coordinates: Coordinates
    address_line1: str = Field(..., description="The first line of the address")
    address_line2: str = Field(None, description="The second line of the address, if applicable")
    city: str = Field(..., description="The city of the address")
    state: str = Field(..., description="The state of the address")
    postal_code: str = Field(..., description="The postal code of the address")


# Define the endpoints with input validation
@address_router.post("/address", response_model=Address)
def create_address(address: Address):
    def create_address(address: AddressCreate):
        db = SessionLocal()
        db_address = Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        db.close()
        return db_address


@address_router.put("/address/{address_id}", response_model=Address)
def update_address(address_id: int, address: Address):
    # Logic to update the address in the database and return the updated address
    pass


@address_router.delete("/address/{address_id}", response_model=Address)
def delete_address(address_id: int):
    # Logic to delete the address from the database and return the deleted address
    pass


@address_router.get("/addresses_within_distance", response_model=List[Address])
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    # Logic to retrieve addresses within the given distance and location coordinates
    pass


# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geopy.distance import geodesic

# Create SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./addresses.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


# Create address model
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)


# Create tables in the database
Base.metadata.create_all(bind=engine)


# Create Pydantic models for request and response
class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float


class AddressUpdate(BaseModel):
    name: str
    latitude: float
    longitude: float


class AddressResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float


# Create CRUD operations for addresses
@app.post("/addresses/", response_model=AddressResponse)
def create_address(address: AddressCreate):
    db = SessionLocal()
    db_address = Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address


@app.put("/addresses/{address_id}", response_model=AddressResponse)
def update_address(address_id: int, address: AddressUpdate):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db_address.name = address.name
    db_address.latitude = address.latitude
    db_address.longitude = address.longitude
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address


@app.delete("/addresses/{address_id}")
def delete_address(address_id: int):
    db = SessionLocal()
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    db.close()
    return {"message": "Address deleted successfully"}


@app.get("/addresses/", response_model=List[AddressResponse])
def get_addresses_within_distance(latitude: float, longitude: float, distance: float):
    db = SessionLocal()
    user_location = (latitude, longitude)
    addresses = db.query(Address).all()
    addresses_within_distance = [
        address for address in addresses
        if geodesic(user_location, (address.latitude, address.longitude)).miles <= distance
    ]
    db.close()
    return addresses_within_distance
