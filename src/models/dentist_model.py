from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Dentist(Base):
    __tablename__ = "dentists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    phone_number = Column(String)
    email = Column(String)

    # Define one-to-many relationship between dentists and appointments
    appointments = relationship("Appointment", back_populates="dentist")