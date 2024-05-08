from fastapi import APIRouter
from . import patients, dentists, treatments, appointments, users, signup, signin, current_user
from fastapi.responses import FileResponse

router = APIRouter()

router.include_router(patients.router, prefix="/patients", tags=["patients"])
router.include_router(dentists.router, prefix="/dentists", tags=["dentists"])
router.include_router(treatments.router, prefix="/treatments", tags=["treatments"])
router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(signup.router, prefix="/signup", tags=["sign_up"])
router.include_router(signin.router, prefix="/token", tags=["sign_in"])
router.include_router(current_user.router, prefix="/current_user", tags=["current_user"])


# root endpoint 
@router.get("/")
def read_root():
    return FileResponse("src/templates/index.html")

# signup_page endpoint 
@router.get("/signup_page")
def read_signup_page():
    return FileResponse("src/templates/signup.html")

# signin_page endpoint 
@router.get("/signin_page")
def read_signin_page():
    return FileResponse("src/templates/signin.html")

# main_about endpoint 
@router.get("/main_about")
def read_main_about_page():
    return FileResponse("src/templates/main_about.html")

# main_dentists endpoint 
@router.get("/main_dentists")
def read_main_dentists_page():
    return FileResponse("src/templates/main_dentists.html")

# main_treatments endpoint 
@router.get("/main_treatments")
def read_main_treatments_page():
    return FileResponse("src/templates/main_treatments.html")

# main_appointments endpoint 
@router.get("/main_appointments")
def read_main_appointments_page():
    return FileResponse("src/templates/main_appointments.html")

# main_appointments endpoint 
@router.get("/main_patient_card")
def read_main_patient_card_page():
    return FileResponse("src/templates/main_patient_card.html")

# main_appointments endpoint 
@router.get("/main_users")
def read_main_users_page():
    return FileResponse("src/templates/main_users.html")