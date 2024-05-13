from fastapi import APIRouter, Depends, HTTPException
from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import treatment_schema
from ..crud import treatment_crud
from ..dependencies import get_current_user, is_admin, mongo_db

router = APIRouter()

# Get the MongoDB collection for treatments
treatments_collection: Collection = mongo_db['treatments']

@router.post("/", response_model=treatment_schema.Treatment)
def create_treatment(treatment_data: treatment_schema.TreatmentCreate, current_user = Depends(get_current_user)):
    if not is_admin(user=current_user):
        raise HTTPException(status_code=403, detail="Only admins can add treatments")
    # Convert treatment_data to dictionary and insert into MongoDB collection
    inserted_id = treatments_collection.insert_one(treatment_data.dict()).inserted_id
    # Retrieve the inserted treatment from MongoDB collection
    new_treatment = treatments_collection.find_one({"_id": inserted_id})
    return new_treatment

@router.get("/{treatment_id}", response_model=treatment_schema.Treatment)
def read_treatment(treatment_id: str):
    # Query MongoDB collection for a treatment by ID
    treatment = treatments_collection.find_one({"_id": ObjectId(treatment_id)})
    if treatment is None:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment

@router.get("/", response_model=list[treatment_schema.Treatment])
def read_treatments(skip: int = 0, limit: int = 100):
    # Retrieve treatments from MongoDB collection with skip and limit
    treatments = treatments_collection.find().skip(skip).limit(limit)
    return list(treatments)

@router.put("/{treatment_id}", response_model=treatment_schema.Treatment)
def update_treatment(treatment_id: str, treatment_data: treatment_schema.TreatmentCreate, current_user = Depends(get_current_user)):
    if not is_admin(user=current_user):
        raise HTTPException(status_code=403, detail="Only admins can update treatments")
    # Update treatment in MongoDB collection
    updated_treatment = treatments_collection.update_one({"_id": ObjectId(treatment_id)}, {"$set": treatment_data.dict()})
    if updated_treatment.modified_count == 0:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment_data

@router.delete("/{treatment_id}", response_model=treatment_schema.Treatment)
def delete_treatment(treatment_id: str, current_user = Depends(get_current_user)):
    if not is_admin(user=current_user):
        raise HTTPException(status_code=403, detail="Only admins can delete treatments")
    # Delete treatment from MongoDB collection
    treatment = treatments_collection.find_one({"_id": ObjectId(treatment_id)})
    deleted_treatment = treatments_collection.delete_one({"_id": ObjectId(treatment_id)})
    if deleted_treatment.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return treatment
