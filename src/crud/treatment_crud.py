from sqlalchemy.orm import Session

from ..models import treatment_model

from ..schemas import treatment_schema


def create_treatment(db: Session, treatment_data: treatment_schema.TreatmentCreate):
    new_treatment = treatment_model.Treatment(**treatment_data.dict())
    db.add(new_treatment)
    db.commit()
    db.refresh(new_treatment)
    return new_treatment

def get_treatment(db: Session, treatment_id: int):
    return db.query(treatment_model.Treatment).filter(treatment_model.Treatment.id == treatment_id).first()

def get_treatments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(treatment_model.Treatment).offset(skip).limit(limit).all()

def update_treatment(db: Session, treatment_id: int, treatment_data: treatment_schema.TreatmentCreate):
    db_treatment = db.query(treatment_model.Treatment).filter(treatment_model.Treatment.id == treatment_id).first()
    if db_treatment:
        for key, value in treatment_data.dict(exclude_unset=True).items():
            setattr(db_treatment, key, value)
        db.commit()
        db.refresh(db_treatment)
        return db_treatment

def delete_treatment(db: Session, treatment_id: int):
    db_treatment = db.query(treatment_model.Treatment).filter(treatment_model.Treatment.id == treatment_id).first()
    if db_treatment:
        db.delete(db_treatment)
        db.commit()
        return db_treatment

