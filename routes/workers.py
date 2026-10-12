from fastapi import Depends, APIRouter, status
from database import get_db
from sqlalchemy.orm import Session
from dependencies import get_currentUser, require_permissions
from schema.worker_schema import (
    create_workers,update_workers, create_vitals, update_vitals, create_records, update_records, schedule_manage,
    login_worker, schedule_update, create_offense, update_offense, create_permission, update_permission,return_worker
)
from uuid import UUID as PyUUID
import services.workers_services as worker_services
from datetime import datetime

worker_router = APIRouter()


@worker_router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login(worker: login_worker, db: Session = Depends(get_db)):
    return worker_services.login_user(db, user=worker)

@worker_router.post("/", status_code=status.HTTP_201_CREATED)
def create_worker(worker: create_workers, db: Session = Depends(get_db)):
    return worker_services.create_workers(db, worker)

@worker_router.get("worker/{worker_id}", status_code=status.HTTP_200_OK,response_model=return_worker)
def get_workers(worker_id: PyUUID,db: Session = Depends(get_db),  currentUser=Depends(require_permissions(["workers.read"])),):
    return worker_services.get_workers(db, worker_id)

#search, multiple workers
@worker_router.get("/", status_code=status.HTTP_200_OK,response_model=list[return_worker])
def get_workers(db: Session = Depends(get_db),  worker_name: str | None = None,
                 role: str | None = None,location_id: PyUUID | None = None, currentUser=Depends(require_permissions(["workers.read"]))):
    return worker_services.get_workers(db,worker_name= worker_name,role= role,location_id=location_id)


@worker_router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def update_worker(worker_id: PyUUID, updates: update_workers, db: Session = Depends(get_db),
                   currentUser=Depends(require_permissions(["workers.update"]))):
    return worker_services.update_worker(db, worker_id, updates)


@worker_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_worker(worker_id: PyUUID, db: Session = Depends(get_db),
                   currentUser=Depends(require_permissions(["workers.delete"]))):
    worker_services.delete_worker(db, worker_id)


# -----------------------------------------------------------------------------------------------------
# Vitals

@worker_router.post("/vitals", status_code=status.HTTP_202_ACCEPTED)
def submit_vitals(work: create_vitals, currentUser=Depends(require_permissions(["vitals.create"])), db: Session = Depends(get_db)):
    return worker_services.submit_vitals(db, work, currentUser.id)


@worker_router.get("/vitals", status_code=status.HTTP_200_OK)
def get_vitals(db: Session = Depends(get_db),currentUser=Depends(get_currentUser), vitals_id: PyUUID | None = None, worker_id: PyUUID | None = None,
                record_id: PyUUID | None = None):
    return worker_services.get_vitals(db, vitals_id=vitals_id, worker_id=worker_id, record_id=record_id)


@worker_router.delete("/vitals", status_code=status.HTTP_204_NO_CONTENT)
def delete_vitals_entry(vitals_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["vitals.delete"]))):
    worker_services.delete_vitals_entry(db, vitals_id)


# -----------------------------------------------------------------------------------------------------
# Records

@worker_router.post("/records", status_code=status.HTTP_202_ACCEPTED)
def submit_records(work: create_records, vitals_id: PyUUID, db: Session = Depends(get_db),
                    currentUser=Depends(require_permissions(["records.create"]))):
    return worker_services.submit_Records(db, currentUser.id, work, vitals_id)


@worker_router.get("/records", status_code=status.HTTP_200_OK)
def get_records(db: Session = Depends(get_db), record_id: PyUUID | None = None, patient_id: PyUUID | None = None,
                 worker_id: PyUUID | None = None,currentUser=Depends(get_currentUser)):
    return worker_services.get_records(db, record_id=record_id, patient_id=patient_id, worker_id=worker_id)


@worker_router.patch("/records", status_code=status.HTTP_202_ACCEPTED)
def update_record(record_id: PyUUID, updates: update_records, db: Session = Depends(get_db),
                   currentUser=Depends(require_permissions(["records.update"]))):
    return worker_services.update_record(db, record_id, updates)


@worker_router.delete("/records", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["records.delete"]))):
    worker_services.delete_record(db, record_id)


# -----------------------------------------------------------------------------------------------------


@worker_router.get("/work", status_code=status.HTTP_200_OK)
def retrieve_work(worker_id: PyUUID, db: Session = Depends(get_db)):
    return worker_services.get_worker_Work(db, worker_id)


@worker_router.delete("/work", status_code=status.HTTP_204_NO_CONTENT)
def delete_work(work_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    worker_services.delete_work(db, work_id)


# -----------------------------------------------------------------------------------------------------
# Schedule

@worker_router.post("/schedule", status_code=status.HTTP_202_ACCEPTED)
def create_schedule(schedule: schedule_manage, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    return worker_services.create_schedule(db, schedule)


@worker_router.get("/schedule", status_code=status.HTTP_200_OK)
def get_schedule(db: Session = Depends(get_db), currentUser=Depends(get_currentUser), worker_id: PyUUID | None = None,
                  time: datetime | None = None, schedule_id: PyUUID | None = None):
    return worker_services.get_schedule(db, worker_id, time, schedule_id)


@worker_router.patch("/schedule", status_code=status.HTTP_202_ACCEPTED)
def update_schedule(schedule_id: PyUUID, updates: schedule_update, db: Session = Depends(get_db),
                     currentUser=Depends(get_currentUser)):
    return worker_services.update_schedule(db, schedule_id, updates)


@worker_router.delete("/schedule", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    worker_services.delete_schedule(db, schedule_id)


# -----------------------------------------------------------------------------------------------------
# Offenses

@worker_router.post("/offenses", status_code=status.HTTP_202_ACCEPTED)
def create_offense(offense: create_offense, db: Session = Depends(get_db),
                    currentUser=Depends(require_permissions(["workers.update"]))):
    return worker_services.create_offense(db, offense)


@worker_router.get("/offenses", status_code=status.HTTP_200_OK)
def get_offenses(db: Session = Depends(get_db), offense_id: PyUUID | None = None, worker_id: PyUUID | None = None,
                  currentUser=Depends(require_permissions(["workers.read"]))):
    return worker_services.get_offenses(db, offense_id=offense_id, worker_id=worker_id)


@worker_router.patch("/offenses", status_code=status.HTTP_202_ACCEPTED)
def update_offense(offense_id: PyUUID, updates: update_offense, db: Session = Depends(get_db),
                    currentUser=Depends(require_permissions(["workers.update"]))):
    return worker_services.update_offense(db, offense_id, updates)


@worker_router.delete("/offenses", status_code=status.HTTP_204_NO_CONTENT)
def delete_offense(offense_id: PyUUID, db: Session = Depends(get_db),
                    currentUser=Depends(require_permissions(["workers.delete"]))):
    worker_services.delete_offense(db, offense_id)


# -----------------------------------------------------------------------------------------------------


@worker_router.post("/permissions", status_code=status.HTTP_202_ACCEPTED)
def create_permission(permission: create_permission, db: Session = Depends(get_db),
                       currentUser=Depends(require_permissions(["permissions.manage"]))):
    return worker_services.create_permission(db, permission)


@worker_router.get("/permissions", status_code=status.HTTP_200_OK)
def get_permissions(db: Session = Depends(get_db), perm_id: int | None = None, role: str | None = None,
                     currentUser=Depends(require_permissions(["permissions.manage"]))):
    return worker_services.get_permissions(db, perm_id=perm_id, role=role)


@worker_router.patch("/permissions", status_code=status.HTTP_202_ACCEPTED)
def update_permission(perm_id: int, updates: update_permission, db: Session = Depends(get_db),
                       currentUser=Depends(require_permissions(["permissions.manage"]))):
    return worker_services.update_permission(db, perm_id, updates)


@worker_router.delete("/permissions", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(perm_id: int, db: Session = Depends(get_db),
                       currentUser=Depends(require_permissions(["permissions.manage"]))):
    worker_services.delete_permission(db, perm_id)
