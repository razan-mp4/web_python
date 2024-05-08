from pydantic import BaseModel


from .appointment_schema import Appointment

class DentistBase(BaseModel):
    name: str
    specialization: str
    phone_number: str
    email: str

class DentistCreate(DentistBase):
    pass

class Dentist(DentistBase):
    id: int
    appointments: list["Appointment"] = []

    class Config:
        orm_mode = True