from enum import Enum
from datetime import datetime
from uuid import UUID as PyUUID
from typing import Optional
from pydantic import BaseModel, Field


class Roles(str, Enum):
    OVERSEER = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
class Gender(str,Enum):
    MALE="male"
    FEMALE="female"

class create_workers(BaseModel):
    name: str
    role: Roles
    password: str
    gender:Gender
    location_id:PyUUID

class login_worker(BaseModel):
    name: str
    password: str

class return_worker(BaseModel):
    id:PyUUID
    name: str
    role: Roles
    gender:Gender
    location_id:PyUUID


class update_workers(BaseModel):
    name: Optional[str] = None
    role: Optional[Roles] = None
    password: Optional[str] = None
    gender:Optional[Gender]= None
    location_id:Optional[PyUUID] = None

# -----------------------------------------------------------------------------------------------------


class schedule_manage(BaseModel):
    start_time: datetime
    end_time: datetime
    worker_id: PyUUID


class schedule_update(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    worker_id: Optional[PyUUID] = None


class create_records(BaseModel):

    date: datetime
    diagnosis: str
    patient_id: PyUUID


class update_records(BaseModel):
    diagnosis: Optional[str] = None


class create_vitals(BaseModel):
    temp: float
    heart: float
    systolic_pressure: int
    diastolic_pressure: int
    patient_id: PyUUID


class update_vitals(BaseModel):
    temp: Optional[float] = None
    heart: Optional[float] = None
    pressure: Optional[str] = Field(default=None, pattern=r"^(\d{3}|\d{2})/(\d{2}|\d{3})$")

# -----------------------------------------------------------------------------------------------------


class create_offense(BaseModel):
    name: str
    demerit_points: int
    worker_id: PyUUID


class update_offense(BaseModel):
    name: Optional[str] = None
    demerit_points: Optional[int] = None


class create_permission(BaseModel):
    role: Roles
    perm: str


class update_permission(BaseModel):
    perm: Optional[str] = None

# -----------------------------------------------------------------------------------------------------
