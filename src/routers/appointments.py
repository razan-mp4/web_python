from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import appointment_schema
from ..crud import appointment_crud, patient_crud
from ..dependencies import get_db, get_current_user, is_admin, is_user

router = APIRouter()

@router.post("/", response_model=appointment_schema.Appointment)
def create_appointment(appointment_data: appointment_schema.AppointmentCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    if is_admin(user=user) or is_user(user=user):
        return appointment_crud.create_appointment(db, appointment_data)
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to create appointments.")

@router.get("/{appointment_id}", response_model=appointment_schema.Appointment)
def read_appointment(appointment_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    db_appointment = appointment_crud.get_appointment(db, appointment_id)
    patient_id = patient_crud.get_patient_id_by_user_id(db, user.id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if is_admin(user=user) or (is_user(user=user) and db_appointment.patient_id == patient_id):
        return db_appointment
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to view this appointment.")

@router.get("/", response_model=list[appointment_schema.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    if is_admin(user=user):
        appointments = appointment_crud.get_appointments(db, skip=skip, limit=limit)
        return appointments
    elif is_user(user=user):
        patient_id = patient_crud.get_patient_id_by_user_id(db, user.id)
        appointments = appointment_crud.get_patient_appointments(db, patient_id, skip=skip, limit=limit)
        return appointments
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to view appointments.")

@router.put("/{appointment_id}", response_model=appointment_schema.Appointment)
def update_appointment(appointment_id: int, appointment_data: appointment_schema.AppointmentUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    if is_admin(user=user):
        updated_appointment = appointment_crud.update_appointment(db, appointment_id, appointment_data)
        if not updated_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return updated_appointment
    db_appointment = appointment_crud.get_appointment(db, appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    patient_id = patient_crud.get_patient_id_by_user_id(db, user.id)
    if db_appointment.patient_id != patient_id:
        raise HTTPException(status_code=403, detail="You don't have permission to update this appointment.")
    updated_appointment = appointment_crud.update_appointment(db, appointment_id, appointment_data)
    return updated_appointment

@router.delete("/{appointment_id}", response_model=appointment_schema.Appointment)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    if is_admin(user=user):
        db_appointment = appointment_crud.delete_appointment(db, appointment_id)
        if db_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return db_appointment
    elif is_user(user=user):
        db_appointment = appointment_crud.get_appointment(db, appointment_id)
        patient_id = patient_crud.get_patient_id_by_user_id(db, user.id)
        if db_appointment is None:
            raise HTTPException(status_code=404, detail="Appointment not found")
        if db_appointment.patient_id == patient_id:
            db_appointment = appointment_crud.delete_appointment(db, appointment_id)
            return db_appointment
        else:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this appointment.")
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to delete appointments.")
