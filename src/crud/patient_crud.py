from pymongo.collection import Collection
from bson.objectid import ObjectId

def get_patient_id_by_user_id(db: Collection, user_id: int):
    # Find patient with the corresponding user_id in MongoDB
    db_patient = db.find_one({"user_id": user_id})
    if db_patient:
        return str(db_patient["_id"])  # Convert ObjectId to string before returning
    return None

def get_patients_by_id(db: Collection, patient_id: str):
    # Find patient with the corresponding patient_id in MongoDB
    patient = db.find_one({"_id": ObjectId(patient_id)})
    return [patient] if patient else []
