from pydantic import BaseModel
from datetime import date
from typing import Optional, List

from .appointment_schema import Appointment


class PatientBase(BaseModel):
    name: str
    address: str
    phone_number: str
    date_of_birth: date
    user_id: Optional[int]


class PatientCreate(PatientBase):
    pass


class Patient(PatientBase):
    id: int
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True
