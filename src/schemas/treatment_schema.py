from pydantic import BaseModel
from bson import ObjectId

class TreatmentBase(BaseModel):
    name: str
    description: str
    price: float

class TreatmentCreate(TreatmentBase):
    pass

class Treatment(TreatmentBase):
    _id: ObjectId  # Use bson.ObjectId for MongoDB's _id field

    class Config:
        orm_mode = True
