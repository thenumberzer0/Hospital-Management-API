from sqlalchemy.orm import Session
from models import Patients, Insurance, PatientFamily, SpecialDetails, Appointments
from fastapi import HTTPException
from uuid import UUID as PyUUID
from datetime import datetime, timedelta
from sqlalchemy import select


def db_search(db: Session, patient_name: str | None = None, age: int | None = None, patient_id: PyUUID | None = None,
              family_id: PyUUID | None = None, insurance_id: PyUUID | None = None, family_name: str | None = None,
              hmo_name: str | None = None):
    if patient_id:
        patient = db.execute(select(Patients).where(Patients.id == patient_id)).scalars().first()
        if not patient:
            raise HTTPException(404, "Patient not Found")
        return patient

    stmt = select(Patients)
    if patient_name:
        stmt = stmt.where(Patients.name.ilike(f"%{patient_name}%"))
    if age:
        stmt = stmt.where(Patients.doB-timedelta(days=age * 365.25) >=0).order_by(Patients.doB)
    if family_id:
        stmt = stmt.where(Patients.family_id == family_id)
    if insurance_id:
        stmt = stmt.where(Patients.insurance_id == insurance_id)
    if hmo_name:
        stmt = stmt.where(Patients.insurance.has(Insurance.name.ilike(f"%{hmo_name}%")))
    if family_name:
        stmt = stmt.where(Patients.family.has(PatientFamily.name.ilike(f"%{family_name}%")))

    return db.execute(stmt).scalars().all()


def get_insurance(db: Session, hmo_id: PyUUID | None = None, hmo_name: str | None = None):
    if hmo_id:
        hmo = db.execute(select(Insurance).where(Insurance.id == hmo_id)).scalars().first()
        if not hmo:
            raise HTTPException(404, "HMO not Found")
        return hmo
    if hmo_name:
        return db.execute(select(Insurance).where(Insurance.name.ilike(f"%{hmo_name}%"))).scalars().all()
    return db.execute(select(Insurance)).scalars().all()


def get_family(db: Session, family_id: PyUUID | None = None, family_name: str | None = None):
    if family_id:
        family = db.execute(select(PatientFamily).where(PatientFamily.id == family_id)).scalars().first()
        if not family:
            raise HTTPException(404, "Family not Found")
        return family
    if family_name:
        return db.execute(select(PatientFamily).where(PatientFamily.name.ilike(f"%{family_name}%"))).scalars().all()
    return db.execute(select(PatientFamily)).scalars().all()


# SpecialDetails (patient allergies / special-care notes)

def db_search_special_details(db: Session, special_id: PyUUID | None = None, patient_id: PyUUID | None = None):
    if special_id:
        item = db.execute(select(SpecialDetails).where(SpecialDetails.id == special_id)).scalars().first()
        if not item:
            raise HTTPException(404, "Item not Found")
        return item

    stmt = select(SpecialDetails)
    if patient_id:
        stmt = stmt.where(SpecialDetails.patient_id == patient_id)
    return db.execute(stmt).scalars().all()


# Appointments

def db_search_appointments(db: Session, appointment_id: PyUUID | None = None, patient_id: PyUUID | None = None,
                            worker_id: PyUUID | None = None, day_time: datetime | None = None):
    if appointment_id:
        item = db.execute(select(Appointments).where(Appointments.id == appointment_id)).scalars().first()
        if not item:
            raise HTTPException(404, "Item not Found")
        return item

    stmt = select(Appointments)
    if patient_id:
        stmt = stmt.where(Appointments.patient_id == patient_id)
    if worker_id:
        stmt = stmt.where(Appointments.worker_id == worker_id)
    if day_time:
        stmt = stmt.where(Appointments.day_time == day_time)
    return db.execute(stmt.order_by(Appointments.day_time.asc())).scalars().all()


def db_add(db: Session, item: Patients | Insurance | PatientFamily | SpecialDetails | Appointments):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception:
        db.rollback()
        raise HTTPException(400, detail="Bad Request")
    return item


def db_delete(db: Session, item: Patients | Insurance | PatientFamily | SpecialDetails | Appointments):
    try:
        db.delete(item)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(404, detail="Item not Found")
