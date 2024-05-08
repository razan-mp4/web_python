from sqlalchemy.orm import Session

from ..models import patient_model

from ..schemas import patient_schema


def create_patient(db: Session, patient_data: patient_schema.PatientCreate):
    new_patient = patient_model.Patient(**patient_data.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

def get_patient(db: Session, patient_id: int):
    return db.query(patient_model.Patient).filter(patient_model.Patient.id == patient_id).first()

def get_patient_by_phone_number_and_address(db: Session, phone_number: str, address: str):
    return db.query(patient_model.Patient).filter(patient_model.Patient.phone_number == phone_number, patient_model.Patient.address == address).first()

def get_patients(db: Session, skip: int = 0, limit: int = 10):
    return db.query(patient_model.Patient).offset(skip).limit(limit).all()

def update_patient(db: Session, patient_id: int, patient_data: patient_schema.PatientCreate):
    db_patient = db.query(patient_model.Patient).filter(patient_model.Patient.id == patient_id).first()
    if db_patient:
        for key, value in patient_data.dict(exclude_unset=True).items():
            setattr(db_patient, key, value)
        db.commit()
        db.refresh(db_patient)
        return db_patient

def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(patient_model.Patient).filter(patient_model.Patient.id == patient_id).first()
    if db_patient:
        db.delete(db_patient)
        db.commit()
        return db_patient

def get_patient_id_by_user_id(db: Session, user_id: int):
    db_patient = db.query(patient_model.Patient).filter(patient_model.Patient.user_id == user_id).first()
    if db_patient:
        return db_patient.id
    return None

def get_patients_by_id(db: Session, patient_id: int):
    return db.query(patient_model.Patient).filter(patient_model.Patient.id == patient_id).all()
