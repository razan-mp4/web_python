from pydantic import BaseModel


class TreatmentBase(BaseModel):
    name: str
    description: str
    price: float

class TreatmentCreate(TreatmentBase):
    pass

class Treatment(TreatmentBase):
    id: int

    class Config:
        orm_mode = True