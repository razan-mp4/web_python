from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite connection
sqlite_engine = create_engine("sqlite:///./sql_app.db")

# PostgreSQL connection
postgresql_engine = create_engine("postgresql://postgres:masterkey@localhost:5432/DentistOffice")

# Session makers
SessionSQLite = sessionmaker(bind=sqlite_engine)
SessionPostgreSQL = sessionmaker(bind=postgresql_engine)



from src.database import Base
from src.models.appointment_model import Appointment
from src.models.dentist_model import Dentist
from src.models.patient_model import Patient
from src.models.user_model import User
from src.models.treatment_model import Treatment

# Define a list of models to migrate
MODELS = [Dentist, Patient, User, Treatment, Appointment]

# Function to migrate data for a single model
def migrate_model_data(model, session_sqlite, session_postgresql):
    sqlite_data = session_sqlite.query(model).all()
    for row in sqlite_data:
        postgresql_row = model(**{column.name: getattr(row, column.name) for column in row.__table__.columns})
        session_postgresql.add(postgresql_row)
    session_postgresql.commit()

# Main function to migrate data for all models
def migrate_data():
    session_sqlite = SessionSQLite()
    session_postgresql = SessionPostgreSQL()
    for model in MODELS:
        migrate_model_data(model, session_sqlite, session_postgresql)
    session_sqlite.close()
    session_postgresql.close()

# Run the migration
if __name__ == "__main__":
    migrate_data()
