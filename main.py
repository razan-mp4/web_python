from fastapi import FastAPI

from src.routers.api import router as api_router


app = FastAPI()



# Include API routers
app.include_router(api_router)
