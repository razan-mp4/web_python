from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from bson import ObjectId

from .appointment_schema import Appointment


class PatientBase(BaseModel):
    name: str
    address: str
    phone_number: str
    date_of_birth: date
    user_id: Optional[str]


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    _id: ObjectId
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True
