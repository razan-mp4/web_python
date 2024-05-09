from sqlalchemy.orm import Session
from ..models import user_model
from ..schemas import user_schema

def create_user(db: Session, user_data: user_schema.UserCreate):
    db_user =  user_model.User(username=user_data.username, email=user_data.email, password=user_data.password, is_active=user_data.is_active, role=user_data.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: user_schema.UserUpdate):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def get_all_users(db: Session) -> list[user_model.User]:
    return db.query(user_model.User).all()


def check_super_admin_exists(db: Session) -> bool:
    super_admin = db.query(user_model.User).filter_by(role='super_admin').first()
    return super_admin is not None

def create_super_admin(db: Session) -> user_model.User:
    if check_super_admin_exists(db):
        return
    super_admin = user_model.User(
        username='super_admin',
        email='super_admin@example.com',
        password='$2b$12$86QXFH/oGwyPdl07a4QzjuchN5B.PKxNLErQbrUbzPnW63KZwEFTK',  # 'superadminpassword'
        role='super_admin',
        is_active=True  # Assuming super admin is always active
    )
    db.add(super_admin)
    db.commit()
    db.refresh(super_admin)
    return super_admin

