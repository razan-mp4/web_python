from fastapi import FastAPI
from src.database import engine, Base
from src.routers.api import router as api_router



Base.metadata.create_all(bind=engine)

app = FastAPI()



# Include API routers
app.include_router(api_router)
