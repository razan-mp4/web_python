from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

from .treatment_schema import Treatment


class AppointmentBase(BaseModel):
    date_and_time: datetime
    notes: str | None = None
    patient_id: str
    dentist_id: str


class AppointmentCreate(AppointmentBase):
    treatment_ids: list[int]

class AppointmentUpdate(AppointmentBase):
    treatment_ids: list[int]


class Appointment(AppointmentBase):
    _id: ObjectId
    treatments: list[Treatment] = []
    

    class Config:
        orm_mode = True

