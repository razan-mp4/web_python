from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional

from .appointment_schema import Appointment

class DentistBase(BaseModel):
    name: str
    specialization: str
    phone_number: str
    email: str

class DentistCreate(DentistBase):
    pass

class Dentist(DentistBase):
    _id: Optional[ObjectId]  # Use bson.ObjectId for MongoDB's _id field
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True
