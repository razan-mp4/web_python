from sqlalchemy.orm import Session

from ..models import dentist_model
from ..schemas import dentist_schema


def create_dentist(db: Session, dentist_data: dentist_schema.DentistCreate):
    new_dentist = dentist_model.Dentist(**dentist_data.dict())
    db.add(new_dentist)
    db.commit()
    db.refresh(new_dentist)
    return new_dentist

def get_dentist(db: Session, dentist_id: int):
    return db.query(dentist_model.Dentist).filter(dentist_model.Dentist.id == dentist_id).first()

def get_dentist_by_email(db: Session, email: str):
    return db.query(dentist_model.Dentist).filter(dentist_model.Dentist.email == email).first()

def get_dentists(db: Session, skip: int = 0, limit: int = 10, dentist_id: int | None = None) -> list[dentist_model.Dentist]:
    query = db.query(dentist_model.Dentist)
    if dentist_id is not None:
        query = query.filter(dentist_model.Dentist.id == dentist_id)
    return query.offset(skip).limit(limit).all()

def update_dentist(db: Session, dentist_id: int, dentist_data: dentist_schema.DentistCreate):
    db_dentist = db.query(dentist_model.Dentist).filter(dentist_model.Dentist.id == dentist_id).first()
    if db_dentist:
        for key, value in dentist_data.dict(exclude_unset=True).items():
            setattr(db_dentist, key, value)
        db.commit()
        db.refresh(db_dentist)
        return db_dentist

def delete_dentist(db: Session, dentist_id: int):
    db_dentist = db.query(dentist_model.Dentist).filter(dentist_model.Dentist.id == dentist_id).first()
    if db_dentist:
        db.delete(db_dentist)
        db.commit()
        return db_dentist
