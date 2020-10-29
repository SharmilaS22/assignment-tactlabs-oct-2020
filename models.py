from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional

#mongodb connect
client = MongoClient('mongodb://localhost:27017/studentDB')
db = client.testDB

#validation of _id
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if ( not ObjectId.is_valid(v) ):
            raise ValueError('Invalid Object id')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

#schema
class Student(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    name: str
    department: str

    class Config:
        arbitary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }