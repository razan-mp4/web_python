from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import patient_schema, user_schema
from ..crud import patient_crud
from ..dependencies import get_current_user, is_admin, is_user, mongo_db

from datetime import datetime

router = APIRouter()

# Get the MongoDB collection for patients
patients_collection: Collection = mongo_db['patients']

@router.post("/", response_model=patient_schema.Patient)
def create_patient(patient_data: patient_schema.PatientCreate):
    # Convert date_of_birth to datetime object
    patient_data.date_of_birth = datetime.combine(patient_data.date_of_birth, datetime.min.time())
    # Insert patient_data into MongoDB patients collection
    inserted_patient = patients_collection.insert_one(patient_data.dict())
    return patient_data

@router.get("/{patient_id}", response_model=patient_schema.Patient)
def read_patient(patient_id: str, current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(patients_collection, current_user["_id"])
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    if is_admin(current_user):
        return patient
    elif is_user(current_user):
        return patient
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access this patient")

@router.get("/", response_model=list[patient_schema.Patient])
def read_patients(skip: int = 0, limit: int = 100, current_user: user_schema.User = Depends(get_current_user)):
    if is_admin(current_user):
        return list(patients_collection.find().skip(skip).limit(limit))
    elif is_user(current_user):
        current_user_patient_id = patient_crud.get_patient_id_by_user_id(patients_collection, current_user["_id"])
        return list(patients_collection.find({"_id": ObjectId(current_user_patient_id)}))
    else:
        raise HTTPException(status_code=403, detail="User not authorized to access patient list")

@router.put("/{patient_id}", response_model=patient_schema.Patient)
def update_patient(patient_id: str, patient_data: patient_schema.PatientCreate, current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(patients_collection, current_user["_id"])
    if is_admin(current_user):
        # Convert date_of_birth to datetime object
        patient_data.date_of_birth = datetime.combine(patient_data.date_of_birth, datetime.min.time())
        # Update patient_data in MongoDB patients collection
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        updated_patient = patients_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": patient_data.dict()})
        if updated_patient.modified_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    elif current_user_patient_id == patient_id:
        # Convert date_of_birth to datetime object
        patient_data.date_of_birth = datetime.combine(patient_data.date_of_birth, datetime.min.time())
        # Update patient_data in MongoDB patients collection
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        updated_patient = patients_collection.update_one({"_id": ObjectId(patient_id)}, {"$set": patient_data.dict()})
        if updated_patient.modified_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    else:
        raise HTTPException(status_code=403, detail="User not authorized to update this patient")



@router.delete("/{patient_id}", response_model=patient_schema.Patient)
def delete_patient(patient_id: str, current_user: user_schema.User = Depends(get_current_user)):
    current_user_patient_id = patient_crud.get_patient_id_by_user_id(patients_collection, current_user["_id"])
    if is_admin(current_user):
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        # Delete patient from MongoDB patients collection
        deleted_patient = patients_collection.delete_one({"_id": ObjectId(patient_id)})
        if deleted_patient.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    elif current_user_patient_id == patient_id:
        patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
        # Delete patient from MongoDB patients collection
        deleted_patient = patients_collection.delete_one({"_id": ObjectId(patient_id)})
        if deleted_patient.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    else:
        raise HTTPException(status_code=403, detail="User not authorized to delete this patient")