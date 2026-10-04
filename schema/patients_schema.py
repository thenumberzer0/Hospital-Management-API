from datetime import datetime
from uuid import UUID as PyUUID
from typing import Optional
from pydantic import BaseModel


class create_patients(BaseModel):
    name: str
    doB: datetime
    address: Optional[str] = None
    phone: Optional[str] = None
    picture_url: Optional[str] = None
    family_id: Optional[PyUUID] = None
    insurance_id: Optional[PyUUID] = None


class update_patients(BaseModel):
    name: Optional[str] = None
    doB: Optional[datetime] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    picture_url: Optional[str] = None
    family_id: Optional[PyUUID] = None
    insurance_id: Optional[PyUUID] = None


# -----------------------------------------------------------------------------------------------------
# SpecialDetails: patient allergy / special-care notes


class create_special_details(BaseModel):
    patient_id: PyUUID
    notes: str


class update_special_details(BaseModel):
    notes: Optional[str] = None


# -----------------------------------------------------------------------------------------------------
# Appointments


class create_appointment(BaseModel):
    patient_id: PyUUID
    day_time: datetime
    doctor_id: Optional[PyUUID] = None


class update_appointment(BaseModel):
    day_time: Optional[datetime] = None
    doctor_id: Optional[PyUUID] = None
