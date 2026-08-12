#search for patients, retrieve them and all their records, updatefrom repos.workers_repo import db_add,db_delete
from fastapi import Depends,APIRouter, status
from schema import create_patients,update_patients
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID 
from database import get_db
from schema import create_patients, update_patients,create_Family,create_insurance,update_insurance,update_family
import services.patients_services as patient_services
#be able to create or edit workers and possible delete
#show things they're responsible for
#make them able to drop things they're responsible for
patient_router = APIRouter()

@patient_router.post("/",status_code=status.HTTP_202_ACCEPTED)
def create_patients(patient:create_patients,db:Session=Depends(get_db)):
    patient_services.create_patients(db,patient)


@patient_router.get("/",status_code=status.HTTP_200_OK)
def get_patients(db:Session=Depends(get_db),patient_name:str|None=None,age:int|None=None,patient_id:PyUUID|None =None,family_id:PyUUID|None=None,insurance_id:PyUUID|None=None,family_name:str|None=None,hmo_name:str|None=None):
    return patient_services.get_patients(db,patient_name=patient_name,patient_id=patient_id,age=age,family_id=family_id,insurance_id=insurance_id,family_name=family_name,hmo_name=hmo_name)

@patient_router.patch("/",status_code=status.HTTP_202_ACCEPTED)
def update_patient(patient_id:PyUUID,updates:update_patients,db:Session=Depends(get_db)):
    patient_services.update_patient(db,patient_id,updates)

@patient_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id:PyUUID,db:Session=Depends(get_db)):
    patient_services.delete_patient(db,patient_id)








@patient_router.post("/group",status_code=status.HTTP_202_ACCEPTED)
def create_group(group:create_insurance|create_Family,db:Session=Depends(get_db)):
    patient_services.create_groups(db,group)


@patient_router.get("/group",status_code=status.HTTP_200_OK)
def get_patients(select_group:bool,db:Session=Depends(get_db), group_name:str|None=None, group_id:PyUUID|None=None):
    return patient_services.get_groups(db,select_group,group_name,group_id)

@patient_router.patch("/group",status_code=status.HTTP_202_ACCEPTED)
def update_patient(updates:update_family|update_insurance,select_group:bool, group_name:str|None=None, group_id:PyUUID|None=None,db:Session=Depends(get_db)):
    patient_services.update_group(db,updates)

@patient_router.delete("/group",status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(select_group:bool, group_name:str|None=None, group_id:PyUUID|None=None,db:Session=Depends(get_db)):
    patient_services.delete_group(db,select_group,group_name,group_id)
