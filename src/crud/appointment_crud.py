from sqlalchemy.orm import Session

from ..models import appointment_model

from ..schemas import appointment_schema
from .treatment_crud import get_treatment


def create_appointment(db: Session, appointment_data: appointment_schema.AppointmentCreate):
    treatment_ids = appointment_data.treatment_ids # Extract treatment IDs
    new_appointment = appointment_model.Appointment(**appointment_data.dict(exclude={'treatment_ids'}))
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    
    # Associate treatments with the appointment
    for treatment_id in treatment_ids:
        treatment = get_treatment(db, treatment_id)
        if treatment:
            new_appointment.treatments.append(treatment)
    
    db.commit()
    return new_appointment

def get_appointment(db: Session, appointment_id: int):
    return db.query(appointment_model.Appointment).filter(appointment_model.Appointment.id == appointment_id).first()

def get_appointments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(appointment_model.Appointment).offset(skip).limit(limit).all()

def update_appointment(db: Session, appointment_id: int, appointment_data: appointment_schema.AppointmentCreate):
    treatment_ids = appointment_data.treatment_ids  # Extract treatment IDs
    db_appointment = db.query(appointment_model.Appointment).filter(appointment_model.Appointment.id == appointment_id).first()
    if db_appointment:
        for key, value in appointment_data.dict(exclude_unset=True).items():
            setattr(db_appointment, key, value)
        # Clear existing treatments and associate new treatments
        db_appointment.treatments.clear()
        for treatment_id in treatment_ids:
            treatment = get_treatment(db, treatment_id)
            if treatment:
                db_appointment.treatments.append(treatment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment

def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(appointment_model.Appointment).filter(appointment_model.Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return db_appointment

def get_patient_appointments(db: Session, patient_id: int, skip: int = 0, limit: int = 10):
    return db.query(appointment_model.Appointment).filter(appointment_model.Appointment.patient_id == patient_id).offset(skip).limit(limit).all()
