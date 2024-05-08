from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=True)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)

    # Define one-to-many relationship between patients and appointments
    appointments = relationship("Appointment", back_populates="patient")
    
    # Define one-to-one relationship with User
    user = relationship("User", back_populates="patient")