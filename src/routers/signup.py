from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..crud import user_crud, patient_crud
from ..schemas import user_schema, patient_schema

from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

@router.post("/", response_model=user_schema.User)
def signup(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):
    super_admin = user_crud.create_super_admin(db)
    # Check if the username or email already exists
    existing_email = user_crud.get_user_by_email(db, email=user_data.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    existing_username = user_crud.get_user_by_username(db, username=user_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    # Hash the password
    user_data.password = pwd_context.hash(user_data.password)

    # Create the new user
    new_user = user_crud.create_user(db, user_data)
    db.commit()
    """
    # If the user is a regular user, search for an existing patient with the provided phone number and address
    if user_data.role == "user":
        existing_patient = patient_crud.get_patient_by_phone_number_and_address(db, phone_number=user_data.phone_number, address=user_data.address)
        if existing_patient:
            # Connect the existing patient to the new user
            existing_patient.user_id = new_user.id
            db.commit()
        else:
            # If no existing patient found, create a new patient and connect it to the user
            new_patient_data = patient_schema.PatientCreate(
                name=user_data.name,
                address=user_data.address,
                phone_number=user_data.phone_number,
                date_of_birth=user_data.date_of_birth,
                user_id=new_user.id
            )
            new_patient = patient_crud.create_patient(db, new_patient_data)
            new_user.patient_id = new_patient.id
            db.commit()
    """
    return new_user