from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import dentist_schema
from ..crud import dentist_crud
from ..dependencies import get_current_user, is_admin, mongo_db

router = APIRouter()

# Get the MongoDB collection for dentists
dentists_collection: Collection = mongo_db['dentists']

@router.post("/", response_model=dentist_schema.Dentist)
def create_dentist(dentist_data: dentist_schema.DentistCreate, current_user: dict = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admins can add dentists")
    db_dentist = dentists_collection.find_one({"email": dentist_data.email})
    if db_dentist:
        raise HTTPException(status_code=400, detail="Email already registered")
    inserted_dentist = dentists_collection.insert_one(dentist_data.dict())
    return dentist_data

@router.put("/{dentist_id}", response_model=dentist_schema.Dentist)
def update_dentist(dentist_id: str, dentist_data: dentist_schema.DentistCreate, current_user: dict = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admins can update dentists")
    existing_dentist = dentists_collection.find_one({"_id": ObjectId(dentist_id)})
    if not existing_dentist:
        raise HTTPException(status_code=404, detail="Dentist not found")
    updated_dentist = dentists_collection.update_one({"_id": ObjectId(dentist_id)}, {"$set": dentist_data.dict()})
    if updated_dentist.modified_count == 0:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return dentist_data

@router.delete("/{dentist_id}", response_model=dentist_schema.Dentist)
def delete_dentist(dentist_id: str, current_user: dict = Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Only admins can delete dentists")
    existing_dentist = dentists_collection.find_one({"_id": ObjectId(dentist_id)})
    if not existing_dentist:
        raise HTTPException(status_code=404, detail="Dentist not found")
    deleted_dentist = dentists_collection.delete_one({"_id": ObjectId(dentist_id)})
    if deleted_dentist.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return existing_dentist

@router.get("/{dentist_id}", response_model=dentist_schema.Dentist)
def read_dentist(dentist_id: str):
    dentist = dentists_collection.find_one({"_id": ObjectId(dentist_id)})
    if not dentist:
        raise HTTPException(status_code=404, detail="Dentist not found")
    return dentist

@router.get("/", response_model=list[dentist_schema.Dentist])
def read_dentists(skip: int = 0, limit: int = 10):
    dentists = dentists_collection.find().skip(skip).limit(limit)
    if not dentists:
        raise HTTPException(status_code=404, detail="Dentists not found")
    return list(dentists)
