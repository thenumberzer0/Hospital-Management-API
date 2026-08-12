#search for patients, retrieve them and all their records, updatefrom repos.workers_repo import db_add,db_delete
from models import Patients, Insurance, PatientFamily
from fastapi import HTTPException
from schema import create_patients,update_patients, create_insurance, create_Family,update_family,update_insurance
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID as PyUUID
from repos.patients_repo import db_add,db_delete, db_search, get_family,get_insurance
#be able to create or edit workers and possible delete
#show things they're responsible for
#make them able to drop things they're responsible for
def get_patients(db:Session,patient_name:str|None=None,age:int|None=None,patient_id:PyUUID|None =None,family_id:PyUUID|None=None,insurance_id:PyUUID|None=None,family_name:str|None=None,hmo_name:str|None=None):
    return db_search(db,patient_name=patient_name,patient_id=patient_id,age=age,family_id=family_id,insurance_id=insurance_id,family_name=family_name,hmo_name=hmo_name)

def create_patients(db:Session,patient:create_patients):
    new_patient=Patients(
        name = patient.name,
        age=patient.age,
        address = patient.address,
        phone=patient.phone,
        family_id =patient.family_id,
        insurance_id = patient.insurance_id
    )
    db_add(db,new_patient)
    return {"Message":"New Patient Made Successfully"}

def update_patient(db:Session,patient_id:PyUUID,updates:update_patients):
    updates = updates.model_dump(exclude_unset=True)
    changed_user= db_search(db,patient_id=patient_id)
    for key, value in updates.items():
        setattr(changed_user, key, value)
    db_add(db,changed_user)
    return{"Message":"Patient Updated!"}

def delete_patient(db:Session,patient_id:PyUUID):
    changed_user= db_search(db,patient_id=patient_id)
    db_delete(db, changed_user)
    return{"Message":"User Deleted"}


def get_groups(db:Session,select_group:bool, group_name:str|None=None, group_id:PyUUID|None=None):
    if(select_group==1):
       return get_family(db,group_id,group_name)
    else:
      return  get_insurance(db,group_id,group_name)

def create_groups(db:Session,group:create_insurance|create_Family):
    if(isinstance(group,create_Family)):
        new_family = PatientFamily(
            name = group.family_name
        )
        db_add(db,new_family)
        return{"Message":"New Family Created"}
    else:
        new_insurance = Insurance(
            name = group.hmo_name
        )
        db_add(db,new_insurance)

def update_group(db:Session,updates:update_family|update_insurance,select_group:bool, group_name:str|None=None, group_id:PyUUID|None=None):
   changed_group = get_groups(db,select_group,group_name,group_id)
   updates = updates.model_dump(exclude_unset=True)
   for key, value in updates.items():
           setattr(changed_group, key, value)
   db_add(db,changed_group)
   return{"Message":"Group Updated!"}



def delete_group(db:Session,select_group:bool, group_name:str|None=None, group_id:PyUUID|None=None):
    changed_group = get_groups(db,select_group,group_name,group_id)
    db_delete(db,changed_group)
    return{"Message":"Group Deleted!"}

