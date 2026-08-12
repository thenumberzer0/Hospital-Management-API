from enum import Enum
from datetime import datetime
from uuid import UUID as PyUUID
from typing import Optional
from pydantic import BaseModel,Field
from datetime import datetime

class Roles(str,Enum):
    OVERSEER = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"


class create_patients(BaseModel):
    name: str
    age: int
    address: Optional[str] = None
    phone: Optional[str] =  None
    family_id:Optional[PyUUID]=None
    insurance_id:Optional[PyUUID]=None

class update_patients(BaseModel):
    name: Optional[str] =  None
    age: Optional[int] = None
    address: Optional[str] = None
    phone: Optional[str] =  None
    family_id:Optional[PyUUID]=None
    insurance_id:Optional[PyUUID]=None

#Workers 
class create_workers(BaseModel):
    name:str
    role:Roles
    password:str

class login_worker(BaseModel):
    name:str
    password:str

class update_workers(BaseModel):
    name:Optional[str] = None
    roles:Optional[Roles] = None
    password:Optional[str] = None


class schedule_manage(BaseModel):
    time:datetime
    worker_id:PyUUID 

class schedule_update(BaseModel):
    time:Optional[datetime]= None
    worker_id:Optional[PyUUID]= None


#Pharmacy Management
class create_pharmacy_items(BaseModel):
    drug_name:str
    batch_number:int
    quantity:int

class update_pharmacy_item(BaseModel):
    drug_name:Optional[str] = None
    batch_number:Optional[int] = None
    quantity:Optional[int] = None


class drugs_used_create(BaseModel):
    drug_id:PyUUID
    record_id:PyUUID
    quantity:int
    date:datetime
    

#Medical Records
class create_records(BaseModel):
    date:datetime
    diagnosis:str
    vitals_id:PyUUID
    patient_id:PyUUID
    date:datetime

class create_vitals(BaseModel):
    temp:float
    heart:float
    pressure:str = Field(pattern=r"^(\d{3}|\d{2})/(\d{2}|\d{3})$")
    date:datetime
    patient_id:PyUUID

class create_insurance(BaseModel):
    hmo_name:str 

class create_Family(BaseModel):
    family_name:str 


class search_family(BaseModel):
    hmo_name:str 

class search_hmo(BaseModel):
    family_name:str 

class update_family(BaseModel):
    family_name:Optional[str] = None
    
class update_insurance(BaseModel):
    hmo_name:Optional[str] = None
