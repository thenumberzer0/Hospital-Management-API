from fastapi import FastAPI
from database import engine
import models
from routes.patients import patient_router
from routes.pharmacy import pharmacy_router
from routes.workers import worker_router
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patient_router,prefix="/patients",tags=["Patients"])
app.include_router(pharmacy_router,prefix="/pharmacy",tags=["Pharmacy"])
app.include_router(worker_router,prefix="/workers",tags=["Workers"])