from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import patient_schema, user_schema
from ..crud import patient_crud
from ..dependencies import get_db, get_current_user, is_admin, is_user


router = APIRouter()


@router.post("/", response_model=patient_schema.Patient)
def create_patient(patient_data: patient_schema.PatientCreate, db: Session = Depends(get_db)):
    #if is_admin(current_user):
    #    return patient_crud.create_patient(db, patient_data)
    #elif is_user(current_user):
    #    raise HTTPException(status_code=400, detail="User already registered as patient")
    #else:
    return patient_crud.create_patient(db, patient_data)

@router.get("/{patient_id}", response_model=patient_schema.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(db, current_user.id)
    if is_admin(current_user):
        return patient_crud.get_patient(db, patient_id)
    elif current_user_patient_id == patient_id:
        return patient_crud.get_patient(db, patient_id)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access this patient")

@router.get("/", response_model=list[patient_schema.Patient])
def read_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(db, current_user.id)
    if is_admin(current_user):
        return patient_crud.get_patients(db, skip=skip, limit=limit)
    elif is_user(current_user):
        return patient_crud.get_patients_by_id(db, current_user_patient_id)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access patient list")

@router.put("/{patient_id}", response_model=patient_schema.Patient)
def update_patient(patient_id: int, patient_data: patient_schema.PatientCreate, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(db, current_user.id)
    if is_admin(current_user):
        return patient_crud.update_patient(db, patient_id, patient_data)
    elif current_user_patient_id == patient_id:
        return patient_crud.update_patient(db, patient_id, patient_data)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to update this patient")

@router.delete("/{patient_id}", response_model=patient_schema.Patient)
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(db, current_user.id)
    if is_admin(current_user):
        return patient_crud.delete_patient(db, patient_id)
    elif current_user_patient_id == patient_id:
        return patient_crud.delete_patient(db, patient_id)
    else:
        raise HTTPException(status_code=403, detail="User not authorized to delete this patient")
