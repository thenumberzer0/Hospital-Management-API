from sqlalchemy.orm import Session
from models import Workers, Record, Vitals, Schedule, Offenses, Permissions,Roles
from fastapi import HTTPException
from uuid import UUID as PyUUID
from sqlalchemy import select
from datetime import datetime


def db_add(db: Session, item: Workers | Record | Vitals | Schedule | Offenses | Permissions):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception:
        db.rollback()
        raise HTTPException(400, detail="Bad Request")
    return item


def db_delete(db: Session, item: Workers | Record | Vitals | Schedule | Offenses | Permissions):
    try:
        db.delete(item)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(404, detail="Item not Found")


def db_search(db: Session, worker_id: PyUUID | None = None, worker_name: str | None = None, role: str | None = None,location_id: PyUUID | None = None):
    if worker_id:
        worker = db.execute(select(Workers).where(Workers.id == worker_id)).scalars().first()
        if not worker:
            raise HTTPException(404, "User not Found")
        return worker

    stmt = select(Workers)
    if worker_name:
        stmt = stmt.where(Workers.name == worker_name)
    if role:
        stmt = stmt.where(Workers.role == role)
    if location_id:
            stmt = stmt.where(Workers.location_id == location_id)    
    return db.execute(stmt).scalars().all()


def get_worker_Work(db: Session, worker_id: PyUUID):
    worker = db.execute(select(Workers).where(Workers.id == worker_id)).scalars().first()
    if not worker:
        raise HTTPException(404, "User not Found")

    if worker.role == Roles.NURSE:
        return worker.vitals
    return worker.records


def gamble_workSearch(db: Session, work_id: PyUUID):
    vitals = db.execute(select(Vitals).where(Vitals.id == work_id)).scalars().first()
    if vitals:
        return vitals

    record = db.execute(select(Record).where(Record.id == work_id)).scalars().first()
    if record:
        return record

    raise HTTPException(404, "Item not found")


def get_aschedule(db: Session, worker_id: PyUUID | None = None, dt: datetime | None = None, schedule_id: PyUUID | None = None):
    stmt = select(Schedule)
    if schedule_id:
        stmt = stmt.where(Schedule.id == schedule_id)
        return db.execute(stmt).scalars().first()
    if worker_id:
        stmt = stmt.where(Schedule.worker_id == worker_id)
    if dt:
        stmt = stmt.where(Schedule.start_time <= dt, Schedule.end_time >= dt)
    return db.execute(stmt).scalars().all()




def db_search_records(db: Session, record_id: PyUUID | None = None, patient_id: PyUUID | None = None,
                       worker_id: PyUUID | None = None):
    if record_id:
        record = db.execute(select(Record).where(Record.id == record_id)).scalars().first()
        if not record:
            raise HTTPException(404, "Record not Found")
        return record

    stmt = select(Record)
    if patient_id:
        stmt = stmt.where(Record.patient_id == patient_id)
    if worker_id:
        stmt = stmt.where(Record.worker_id == worker_id)
    return db.execute(stmt.order_by(Record.date.desc())).scalars().all()


# Vitals (explicit, id-based access)

def db_search_vitals(db: Session, vitals_id: PyUUID | None = None, worker_id: PyUUID | None = None,
                      record_id: PyUUID | None = None):
    if vitals_id:
        vitals = db.execute(select(Vitals).where(Vitals.id == vitals_id)).scalars().first()
        if not vitals:
            raise HTTPException(404, "Vitals not Found")
        return vitals

    stmt = select(Vitals)
    if worker_id:
        stmt = stmt.where(Vitals.worker_id == worker_id)
    if record_id:
        stmt = stmt.where(Vitals.record_id == record_id)
    return db.execute(stmt).scalars().all()


# Offenses

def db_search_offenses(db: Session, offense_id: PyUUID | None = None, worker_id: PyUUID | None = None):
    if offense_id:
        offense = db.execute(select(Offenses).where(Offenses.id == offense_id)).scalars().first()
        if not offense:
            raise HTTPException(404, "Offense not Found")
        return offense

    stmt = select(Offenses)
    if worker_id:
        stmt = stmt.where(Offenses.worker_id == worker_id)
    return db.execute(stmt).scalars().all()


# Permissions

def db_search_permissions(db: Session, perm_id: int | None = None, role: str | None = None):
    if perm_id:
        perm = db.execute(select(Permissions).where(Permissions.id == perm_id)).scalars().first()
        if not perm:
            raise HTTPException(404, "Permission not Found")
        return perm

    stmt = select(Permissions)
    if role:
        stmt = stmt.where(Permissions.role == role)
    return db.execute(stmt).scalars().all()
