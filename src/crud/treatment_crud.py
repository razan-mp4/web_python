from pymongo.collection import Collection
from bson.objectid import ObjectId
from ..schemas import treatment_schema

def create_treatment(db: Collection, treatment_data: treatment_schema.TreatmentCreate):
    new_treatment = treatment_data.dict()
    # Insert the treatment into the MongoDB collection
    treatment_id = db.insert_one(new_treatment).inserted_id
    new_treatment['_id'] = treatment_id
    return new_treatment

def get_treatment(db: Collection, treatment_id: str):
    return db.find_one({"_id": ObjectId(treatment_id)})

def get_treatments(db: Collection, skip: int = 0, limit: int = 100):
    return list(db.find().skip(skip).limit(limit))

def update_treatment(db: Collection, treatment_id: str, treatment_data: treatment_schema.TreatmentCreate):
    # Prepare updated treatment data
    updated_treatment = treatment_data.dict(exclude_unset=True)
    # Update the treatment in the MongoDB collection
    db.update_one({"_id": ObjectId(treatment_id)}, {"$set": updated_treatment})
    # Return the updated treatment
    return get_treatment(db, treatment_id)

def delete_treatment(db: Collection, treatment_id: str):
    treatment = get_treatment(db, treatment_id)
    if treatment:
        db.delete_one({"_id": ObjectId(treatment_id)})
    return treatment
