from sqlalchemy.orm import Session
from ..models import user_model
from ..schemas import user_schema

def create_user(db: Session, user_data: user_schema.UserCreate):
    db_user =  user_model.User(username=user_data.username, email=user_data.email, password=user_data.password, is_active=user_data.is_active, role=user_data.role)
    db.add(db_user)
    db.commit()
