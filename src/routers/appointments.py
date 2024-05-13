from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import appointment_schema
from ..crud import appointment_crud, patient_crud
from ..dependencies import get_current_user, mongo_db

router = APIRouter()

# Get the MongoDB collection for appointments
appointments_collection: Collection = mongo_db['appointments']

@router.post("/", response_model=appointment_schema.Appointment)
def create_appointment(appointment_data: appointment_schema.AppointmentCreate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    user_role = current_user.get("role")
    if user_role == "admin" or user_role == "user":
        return appointment_crud.create_appointment(appointments_collection, appointment_data)
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to create appointments.")

@router.get("/{appointment_id}", response_model=appointment_schema.Appointment)
def read_appointment(appointment_id: str):
    appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@router.get("/", response_model=list[appointment_schema.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    user_role = current_user.get("role")
    if user_role == "admin":
        appointments = appointment_crud.get_appointments(appointments_collection, skip=skip, limit=limit)
        return appointments
    elif user_role == "user":
        patient_id = current_user.get("patient_id")
        appointments = appointment_crud.get_patient_appointments(appointments_collection, patient_id, skip=skip, limit=limit)
        return appointments
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to view appointments.")

@router.put("/{appointment_id}", response_model=appointment_schema.Appointment)
def update_appointment(appointment_id: str, appointment_data: appointment_schema.AppointmentUpdate, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    user_role = current_user.get("role")
    if user_role == "admin":
        updated_appointment = appointment_crud.update_appointment(appointments_collection, appointment_id, appointment_data)
        if not updated_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return updated_appointment
    else:
        appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        if current_user.get("patient_id") != appointment.get("patient_id"):
            raise HTTPException(status_code=403, detail="You don't have permission to update this appointment.")
        updated_appointment = appointment_crud.update_appointment(appointments_collection, appointment_id, appointment_data)
        return updated_appointment

@router.delete("/{appointment_id}", response_model=appointment_schema.Appointment)
def delete_appointment(appointment_id: str, current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized. Please log in.")
    user_role = current_user.get("role")
    if user_role == "admin":
        deleted_appointment = appointment_crud.delete_appointment(appointments_collection, appointment_id)
        if not deleted_appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return deleted_appointment
    elif user_role == "user":
        appointment = appointments_collection.find_one({"_id": ObjectId(appointment_id)})
        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")
        if current_user.get("patient_id") != appointment.get("patient_id"):
            raise HTTPException(status_code=403, detail="You don't have permission to delete this appointment.")
        deleted_appointment = appointment_crud.delete_appointment(appointments_collection, appointment_id)
        return deleted_appointment
    else:
        raise HTTPException(status_code=403, detail="You don't have permission to delete appointments.")
