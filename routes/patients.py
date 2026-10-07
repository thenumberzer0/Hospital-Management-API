from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID
from datetime import datetime
from database import get_db
from dependencies import get_currentUser,require_permissions
from schema.patients_schema import (
   create_patients, update_patients, create_Family, create_insurance, update_insurance, update_family,
    create_special_details, update_special_details, create_appointment, update_appointment,
)
import services.patients_services as patient_services

patient_router = APIRouter()


@patient_router.post("/", status_code=status.HTTP_202_ACCEPTED)
def create_patients(patient: create_patients, db: Session = Depends(get_db),currentUser=Depends(get_currentUser)):
    return patient_services.create_patient(db, patient)


@patient_router.get("/", status_code=status.HTTP_200_OK)
def get_patients(db: Session = Depends(get_db), patient_name: str | None = None, age: int | None = None,
                  patient_id: PyUUID | None = None, family_id: PyUUID | None = None, insurance_id: PyUUID | None = None,
                  family_name: str | None = None, hmo_name: str | None = None,currentUser=Depends(get_currentUser)):
    return patient_services.get_patients(db, patient_name=patient_name, patient_id=patient_id, age=age,
                                          family_id=family_id, insurance_id=insurance_id, family_name=family_name,
                                          hmo_name=hmo_name)


@patient_router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def update_patient(patient_id: PyUUID, updates: update_patients, db: Session = Depends(get_db),
                    currentUser=Depends(get_currentUser)):
    return patient_services.update_patient(db, patient_id, updates)


@patient_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    patient_services.delete_patient(db, patient_id)


@patient_router.post("/group", status_code=status.HTTP_202_ACCEPTED)
def create_group(group: create_insurance | create_Family, db: Session = Depends(get_db),
                  currentUser=Depends(get_currentUser)):
    return patient_services.create_groups(db, group)


@patient_router.get("/group", status_code=status.HTTP_200_OK)
def get_groups(select_group: bool, db: Session = Depends(get_db), group_name: str | None = None,
                group_id: PyUUID | None = None,currentUser=Depends(get_currentUser)):
    return patient_services.get_groups(db, select_group, group_name, group_id)


@patient_router.patch("/group", status_code=status.HTTP_202_ACCEPTED)
def update_group(updates: update_family | update_insurance, select_group: bool, group_name: str | None = None,
                  group_id: PyUUID | None = None, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["groups.update"]))):
    return patient_services.update_group(db, updates, select_group, group_name, group_id)


@patient_router.delete("/group", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(select_group: bool, group_name: str | None = None, group_id: PyUUID | None = None,
                  db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    patient_services.delete_group(db, select_group, group_name, group_id)


# -----------------------------------------------------------------------------------------------------

@patient_router.post("/allergies", status_code=status.HTTP_202_ACCEPTED)
def create_allergy(item: create_special_details, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    return patient_services.create_special_details(db, item)


@patient_router.get("/allergies", status_code=status.HTTP_200_OK)
def get_allergies(db: Session = Depends(get_db), special_id: PyUUID | None = None, patient_id: PyUUID | None = None,currentUser=Depends(get_currentUser)):
    return patient_services.get_special_details(db, special_id=special_id, patient_id=patient_id)


@patient_router.patch("/allergies", status_code=status.HTTP_202_ACCEPTED)
def update_allergy(special_id: PyUUID, updates: update_special_details, db: Session = Depends(get_db),
                    currentUser=Depends(get_currentUser)):
    return patient_services.update_special_details(db, special_id, updates)


@patient_router.delete("/allergies", status_code=status.HTTP_204_NO_CONTENT)
def delete_allergy(special_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    patient_services.delete_special_details(db, special_id)


# -----------------------------------------------------------------------------------------------------
# Appointments

@patient_router.post("/appointments", status_code=status.HTTP_202_ACCEPTED)
def create_appointment_route(appointment: create_appointment, db: Session = Depends(get_db),
                              currentUser=Depends(get_currentUser)):
    return patient_services.create_appointment(db, appointment)


@patient_router.get("/appointments", status_code=status.HTTP_200_OK)
def get_appointments(db: Session = Depends(get_db), appointment_id: PyUUID | None = None,
                      patient_id: PyUUID | None = None, worker_id: PyUUID | None = None,
                      day_time: datetime | None = None,currentUser=Depends(get_currentUser)):
    return patient_services.get_appointments(db, appointment_id=appointment_id, patient_id=patient_id,
                                              worker_id=worker_id, day_time=day_time)


@patient_router.patch("/appointments", status_code=status.HTTP_202_ACCEPTED)
def update_appointment_route(appointment_id: PyUUID, updates: update_appointment, db: Session = Depends(get_db),
                              currentUser=Depends(get_currentUser)):
    return patient_services.update_appointment(db, appointment_id, updates)


@patient_router.delete("/appointments", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment_route(appointment_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    patient_services.delete_appointment(db, appointment_id)
