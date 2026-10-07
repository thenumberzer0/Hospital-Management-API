from repos.workers_repo import (
    db_add, db_delete, db_search, gamble_workSearch, get_aschedule,
    db_search_records, db_search_vitals, db_search_offenses, db_search_permissions,
)
from repos.workers_repo import get_worker_Work as _get_worker_Work_repo
from models import Workers, Record, Vitals, Schedule, Permissions, Offenses
from fastapi import HTTPException, Response
from auth import hash_password, verify_password, create_access_token
from schema import (
    create_workers, update_workers, create_vitals, update_vitals, create_records, update_records,
    schedule_manage, login_worker, schedule_update, create_offense, update_offense,
    create_permission, update_permission,
)
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID as PyUUID
from datetime import datetime


def create_workers(db: Session, worker: create_workers):
    new_worker = Workers(
        name=worker.name,
        role=worker.role,
        hashed_password=hash_password(worker.password),
        gender = worker.gender,
        location_id = worker.location_id
    )
    db_add(db, new_worker)
    return {"Message": "New Worker Made Successfully", "id": new_worker.id}


def login_user(db: Session, user: login_worker,response:Response):
    found = db_search(db, worker_name=user.name)
    matches = list(found) if isinstance(found, list) else [found]
    if not matches or matches[0] is None:
        raise HTTPException(401, "Wrong Credentials")
    sus_user = matches[0]

    if not verify_password(user.password, sus_user.hashed_password):
        raise HTTPException(401, "Wrong Credentials")

    user_permissions = db.execute(
        select(Permissions.perm).where(Permissions.role == sus_user.role)
    ).scalars().all()

    token_jwt = create_access_token(data={
        "user_id": str(sus_user.id),
        "permissions": list(user_permissions),
    })
    refresh_jwt = create_access_token(data={"user_id": str(sus_user.id)})
    response.set_cookie(key="token",value=token_jwt,httponly=True,samesite="lax",secure=True)
    return {"access_token": token_jwt, "token_type": "bearer"}



def get_workers(db: Session, worker_id: PyUUID | None = None, worker_name: str | None = None, role: str | None = None,location_id: PyUUID | None = None):
    return db_search(db, worker_id, worker_name, role,location_id)


def update_worker(db: Session, worker_id: PyUUID, updates: update_workers):
    changed_worker = db_search(db, worker_id=worker_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        if key == "password":
            changed_worker.hashed_password = hash_password(value)
        else:
            setattr(changed_worker, key, value)
    db_add(db, changed_worker)
    return {"Message": "Worker Updated!"}


def delete_worker(db: Session, worker_id: PyUUID):
    changed_worker = db_search(db, worker_id=worker_id)
    db_delete(db, changed_worker)
    return {"Message": "Worker Deleted Successfully"}


# -----------------------------------------------------------------------------------------------------
# Vitals
    temp: float
    heart: float
    systolic_pressure: int
    diastolic_pressure: int

def submit_vitals(db: Session, work: create_vitals, user: PyUUID):
    vitals = Vitals(
        temp=work.temp,
        heart=work.heart,
        systolic_pressure=work.systolic_pressure,
        diastolic_pressure=work.diastolic_pressure,
        worker_id=user
    )
    db_add(db, vitals)
    return {"Message": "Vitals uploaded", "vitals_id": vitals.id}


def get_vitals(db: Session, vitals_id: PyUUID | None = None, worker_id: PyUUID | None = None,
                record_id: PyUUID | None = None):
    return db_search_vitals(db, vitals_id=vitals_id, worker_id=worker_id, record_id=record_id)


def update_vitals_entry(db: Session, vitals_id: PyUUID, updates: update_vitals):
    changed_vitals = db_search_vitals(db, vitals_id=vitals_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_vitals, key, value)
    db_add(db, changed_vitals)
    return {"Message": "Vitals Updated!"}


def delete_vitals_entry(db: Session, vitals_id: PyUUID):
    changed_vitals = db_search_vitals(db, vitals_id=vitals_id)
    db_delete(db, changed_vitals)
    return {"Message": "Vitals Deleted"}


# -----------------------------------------------------------------------------------------------------
# Records

def submit_Records(db: Session, user: PyUUID, work: create_records, vitals_id: PyUUID):
    record = Record(
        date=work.date,
        diagnosis=work.diagnosis,
        worker_id=user,
        patient_id=work.patient_id,
    )
    db_add(db, record)

    # Record has no vitals_id column — Vitals points at Record instead, so
    # link the already-submitted vitals row to the new record here.
    vitals = db.execute(select(Vitals).where(Vitals.id == vitals_id)).scalars().first()
    if not vitals:
        raise HTTPException(404, "Vitals not found")
    vitals.record_id = record.id
    db_add(db, vitals)

    return {"Message": "Record Uploaded", "record_id": record.id}


def get_records(db: Session, record_id: PyUUID | None = None, patient_id: PyUUID | None = None,
                 worker_id: PyUUID | None = None):
    return db_search_records(db, record_id=record_id, patient_id=patient_id, worker_id=worker_id)


def update_record(db: Session, record_id: PyUUID, updates: update_records):
    changed_record = db_search_records(db, record_id=record_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_record, key, value)
    db_add(db, changed_record)
    return {"Message": "Record Updated!"}


def delete_record(db: Session, record_id: PyUUID):
    changed_record = db_search_records(db, record_id=record_id)
    db_delete(db, changed_record)
    return {"Message": "Record Deleted"}


# -----------------------------------------------------------------------------------------------------

def get_worker_Work(db: Session, worker_id: PyUUID):
    return _get_worker_Work_repo(db, worker_id)


def delete_work(db: Session, work_id: PyUUID):
    work = gamble_workSearch(db, work_id)
    db_delete(db, work)
    return {"Message": "Job deleted", "id": work.id}


# -----------------------------------------------------------------------------------------------------
# Schedule

def create_schedule(db: Session, schedule: schedule_manage):
    new_schedule = Schedule(
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        worker_id=schedule.worker_id
    )
    db_add(db, new_schedule)
    return {"Message": "Schedule Created!", "id": new_schedule.id}


def get_schedule(db: Session, worker_id: PyUUID | None = None, time: datetime | None = None, schedule_id: PyUUID | None = None):
    return get_aschedule(db, worker_id, time, schedule_id)


def update_schedule(db: Session, schedule_id: PyUUID, updates: schedule_update):
    result = get_aschedule(db, schedule_id=schedule_id)
    if not result:
        raise HTTPException(404, "Schedule not found")
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(result, key, value)
    db_add(db, result)
    return {"Message": "Worker Schedule Updated!"}


def delete_schedule(db: Session, schedule_id: PyUUID):
    result = get_aschedule(db, schedule_id=schedule_id)
    if not result:
        raise HTTPException(404, "Schedule not found")
    db_delete(db, result)
    return {"Message": "Schedule Deleted!"}


# -----------------------------------------------------------------------------------------------------
# Offenses

def get_offenses(db: Session, offense_id: PyUUID | None = None, worker_id: PyUUID | None = None):
    return db_search_offenses(db, offense_id=offense_id, worker_id=worker_id)


def create_offense(db: Session, offense: create_offense):
    new_offense = Offenses(
        name=offense.name,
        demerit_points=offense.demerit_points,
        worker_id=offense.worker_id,
    )
    db_add(db, new_offense)
    return {"Message": "Offense Logged", "id": new_offense.id}


def update_offense(db: Session, offense_id: PyUUID, updates: update_offense):
    changed_offense = db_search_offenses(db, offense_id=offense_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_offense, key, value)
    db_add(db, changed_offense)
    return {"Message": "Offense Updated!"}


def delete_offense(db: Session, offense_id: PyUUID):
    changed_offense = db_search_offenses(db, offense_id=offense_id)
    db_delete(db, changed_offense)
    return {"Message": "Offense Deleted"}


# -----------------------------------------------------------------------------------------------------
# Permissions

def get_permissions(db: Session, perm_id: int | None = None, role: str | None = None):
    return db_search_permissions(db, perm_id=perm_id, role=role)


def create_permission(db: Session, permission: create_permission):
    new_permission = Permissions(role=permission.role, perm=permission.perm)
    db_add(db, new_permission)
    return {"Message": "Permission Granted", "id": new_permission.id}


def update_permission(db: Session, perm_id: int, updates: update_permission):
    changed_permission = db_search_permissions(db, perm_id=perm_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_permission, key, value)
    db_add(db, changed_permission)
    return {"Message": "Permission Updated!"}


def delete_permission(db: Session, perm_id: int):
    changed_permission = db_search_permissions(db, perm_id=perm_id)
    db_delete(db, changed_permission)
    return {"Message": "Permission Revoked"}
