from models import Patients, Insurance, PatientFamily, SpecialDetails, Appointments
from schema import (
    create_patients, update_patients, create_insurance, create_Family, update_family, update_insurance,
    create_special_details, update_special_details, create_appointment, update_appointment,
)
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID
from datetime import datetime
from repos.patients_repo import (
    db_add, db_delete, db_search, get_family, get_insurance,
    db_search_special_details, db_search_appointments,
)


def get_patients(db: Session, patient_name: str | None = None, age: int | None = None, patient_id: PyUUID | None = None,
                  family_id: PyUUID | None = None, insurance_id: PyUUID | None = None, family_name: str | None = None,
                  hmo_name: str | None = None):
    return db_search(db, patient_name=patient_name, patient_id=patient_id, age=age, family_id=family_id,
                      insurance_id=insurance_id, family_name=family_name, hmo_name=hmo_name)


def create_patients(db: Session, patient: create_patients):
    new_patient = Patients(
        name=patient.name,
        doB=patient.doB,
        address=patient.address,
        phone=patient.phone,
        picture_url=patient.picture_url,
        family_id=patient.family_id,
        insurance_id=patient.insurance_id,
    )
    db_add(db, new_patient)
    return {"Message": "New Patient Made Successfully", "id": new_patient.id}


def update_patient(db: Session, patient_id: PyUUID, updates: update_patients):
    changed_patient = db_search(db, patient_id=patient_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_patient, key, value)
    db_add(db, changed_patient)
    return {"Message": "Patient Updated!"}


def delete_patient(db: Session, patient_id: PyUUID):
    changed_patient = db_search(db, patient_id=patient_id)
    db_delete(db, changed_patient)
    return {"Message": "Patient Deleted"}


def get_groups(db: Session, select_group: bool, group_name: str | None = None, group_id: PyUUID | None = None):
    if select_group:
        return get_family(db, group_id, group_name)
    return get_insurance(db, group_id, group_name)


def create_groups(db: Session, group: create_insurance | create_Family):
    if isinstance(group, create_Family):
        new_family = PatientFamily(name=group.family_name)
        db_add(db, new_family)
        return {"Message": "New Family Created", "id": new_family.id}

    new_insurance = Insurance(name=group.hmo_name)
    db_add(db, new_insurance)
    return {"Message": "New Insurance Created", "id": new_insurance.id}


def update_group(db: Session, updates: update_family | update_insurance, select_group: bool,
                  group_name: str | None = None, group_id: PyUUID | None = None):
    changed_group = get_groups(db, select_group, group_name, group_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        target_key = "name" if key in ("hmo_name", "family_name") else key
        setattr(changed_group, target_key, value)
    db_add(db, changed_group)
    return {"Message": "Group Updated!"}


def delete_group(db: Session, select_group: bool, group_name: str | None = None, group_id: PyUUID | None = None):
    changed_group = get_groups(db, select_group, group_name, group_id)
    db_delete(db, changed_group)
    return {"Message": "Group Deleted!"}


# -----------------------------------------------------------------------------------------------------
# SpecialDetails (patient allergies / special-care notes)

def get_special_details(db: Session, special_id: PyUUID | None = None, patient_id: PyUUID | None = None):
    return db_search_special_details(db, special_id=special_id, patient_id=patient_id)


def create_special_details(db: Session, item: create_special_details):
    new_item = SpecialDetails(patient_id=item.patient_id, notes=item.notes)
    db_add(db, new_item)
    return {"Message": "Allergy/Special Detail Added", "id": new_item.id}


def update_special_details(db: Session, special_id: PyUUID, updates: update_special_details):
    changed_item = db_search_special_details(db, special_id=special_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_item, key, value)
    db_add(db, changed_item)
    return {"Message": "Allergy/Special Detail Updated!"}


def delete_special_details(db: Session, special_id: PyUUID):
    changed_item = db_search_special_details(db, special_id=special_id)
    db_delete(db, changed_item)
    return {"Message": "Allergy/Special Detail Deleted"}


# -----------------------------------------------------------------------------------------------------
# Appointments

def get_appointments(db: Session, appointment_id: PyUUID | None = None, patient_id: PyUUID | None = None,
                      doctor_id: PyUUID | None = None, day_time: datetime | None = None):
    return db_search_appointments(db, appointment_id=appointment_id, patient_id=patient_id, doctor_id=doctor_id,
                                   day_time=day_time)


def create_appointment(db: Session, appointment: create_appointment):
    new_appointment = Appointments(
        patient_id=appointment.patient_id,
        day_time=appointment.day_time,
        doctor_id=appointment.doctor_id,
    )
    db_add(db, new_appointment)
    return {"Message": "Appointment Booked", "id": new_appointment.id}


def update_appointment(db: Session, appointment_id: PyUUID, updates: update_appointment):
    changed_appointment = db_search_appointments(db, appointment_id=appointment_id)
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed_appointment, key, value)
    db_add(db, changed_appointment)
    return {"Message": "Appointment Updated!"}


def delete_appointment(db: Session, appointment_id: PyUUID):
    changed_appointment = db_search_appointments(db, appointment_id=appointment_id)
    db_delete(db, changed_appointment)
    return {"Message": "Appointment Cancelled"}
