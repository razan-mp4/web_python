from pydantic import BaseModel

from datetime import datetime

from .treatment_schema import Treatment


class AppointmentBase(BaseModel):
    date_and_time: datetime
    notes: str | None = None
    patient_id: int
    dentist_id: int


class AppointmentCreate(AppointmentBase):
    treatment_ids: list[int]

class AppointmentUpdate(AppointmentBase):
    treatment_ids: list[int]


class Appointment(AppointmentBase):
    id: int
    treatments: list[Treatment] = []
    

    class Config:
        orm_mode = True

