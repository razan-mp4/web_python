from pymongo.collection import Collection
from pymongo.results import InsertOneResult, DeleteResult, UpdateResult
from bson import ObjectId
from ..schemas import dentist_schema
from typing import Optional, List

def create_dentist(db: Collection, dentist_data: dentist_schema.DentistCreate) -> Optional[dict]:
    new_dentist_data = dentist_data.dict()
    result: InsertOneResult = db.insert_one(new_dentist_data)
    if result.inserted_id:
        new_dentist_data["_id"] = result.inserted_id
        return new_dentist_data
    return None

def get_dentist(db: Collection, dentist_id: str) -> Optional[dict]:
    dentist = db.find_one({"_id": ObjectId(dentist_id)})
    return dentist

def get_dentist_by_email(db: Collection, email: str) -> Optional[dict]:
    dentist = db.find_one({"email": email})
    return dentist

def get_dentists(db: Collection, skip: int = 0, limit: int = 10, dentist_id: str = None) -> List[dict]:
    query = {}  # Query to filter documents, you can add more filters as needed
    if dentist_id:
        query["_id"] = ObjectId(dentist_id)
    dentists = db.find(query).skip(skip).limit(limit)
    return list(dentists)

def update_dentist(db: Collection, dentist_id: str, dentist_data: dentist_schema.DentistCreate) -> Optional[dict]:
    updated_dentist_data = dentist_data.dict(exclude_unset=True)
    result: UpdateResult = db.update_one({"_id": ObjectId(dentist_id)}, {"$set": updated_dentist_data})
    if result.modified_count > 0:
        updated_dentist = db.find_one({"_id": ObjectId(dentist_id)})
        return updated_dentist
    return None

def delete_dentist(db: Collection, dentist_id: str) -> Optional[dict]:
    result: DeleteResult = db.delete_one({"_id": ObjectId(dentist_id)})
    if result.deleted_count > 0:
        deleted_dentist = {"_id": dentist_id}  # Return the ID of the deleted dentist
        return deleted_dentist
    return None
