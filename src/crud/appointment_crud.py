from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import appointment_schema
from .treatment_crud import get_treatment

def create_appointment(db: Collection, appointment_data: appointment_schema.AppointmentCreate):
    treatment_ids = appointment_data.treatment_ids
    new_appointment = appointment_data.dict(exclude={'treatment_ids'})
    # Associate treatments with the appointment
    new_appointment['treatments'] = []
    for treatment_id in treatment_ids:
        treatment = get_treatment(db, treatment_id)
        if treatment:
            new_appointment['treatments'].append(treatment)
    # Insert the appointment into the MongoDB collection
    appointment_id = db.insert_one(new_appointment).inserted_id
    new_appointment['_id'] = appointment_id
    return new_appointment

def get_appointment(db: Collection, appointment_id: str):
    return db.find_one({"_id": ObjectId(appointment_id)})

def get_appointments(db: Collection, skip: int = 0, limit: int = 100):
    return list(db.find().skip(skip).limit(limit))

def update_appointment(db: Collection, appointment_id: str, appointment_data: appointment_schema.AppointmentCreate):
    treatment_ids = appointment_data.treatment_ids
    # Prepare updated appointment data
    updated_appointment = appointment_data.dict(exclude_unset=True)
    updated_appointment['treatments'] = []
    for treatment_id in treatment_ids:
        treatment = get_treatment(db, treatment_id)
        if treatment:
            updated_appointment['treatments'].append(treatment)
    # Update the appointment in the MongoDB collection
    db.update_one({"_id": ObjectId(appointment_id)}, {"$set": updated_appointment})
    # Return the updated appointment
    return get_appointment(db, appointment_id)

def delete_appointment(db: Collection, appointment_id: str):
    appointment = get_appointment(db, appointment_id)
    if appointment:
        db.delete_one({"_id": ObjectId(appointment_id)})
    return appointment

def get_patient_appointments(db: Collection, patient_id: int, skip: int = 0, limit: int = 10):
    return list(db.find({"patient_id": patient_id}).skip(skip).limit(limit))
