from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

from ..database import Base

# Define association table for appointments and treatments
appointment_treatment_association = Table(
    'appointment_treatment_association', Base.metadata,
    Column('appointment_id', Integer, ForeignKey('appointments.id')),
    Column('treatment_id', Integer, ForeignKey('treatments.id'))
)

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_and_time = Column(DateTime, default=datetime.now())
    dentist_id = Column(Integer, ForeignKey('dentists.id'))
    notes = Column(String)

    # Define many-to-one relationship between appointments and patients
    patient = relationship("Patient", back_populates="appointments")

    # Define many-to-one relationship between appointments and dentists
    dentist = relationship("Dentist", back_populates="appointments")

    # Define many-to-many relationship between appointments and treatments
    treatments = relationship("Treatment", secondary=appointment_treatment_association)

