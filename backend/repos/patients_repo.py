from sqlalchemy.orm import Session
from models import Patients, Insurance, PatientFamily
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID as PyUUID
from sqlalchemy import select


def db_search(db:Session,patient_name:str|None=None,age:int|None=None,patient_id:PyUUID|None =None,family_id:PyUUID|None=None,insurance_id:PyUUID|None=None,family_name:str|None=None,hmo_name:str|None=None):
       if(patient_id):
        try:
            stmt = select(Patients).where(Patients.id==patient_id)
            patient = db.execute(stmt).scalars().first()
            return patient
        except:
            raise HTTPException(404,"User not Found")
       stmt = select(Patients)
       if(patient_name):
            stmt = stmt.where(Patients.name.ilike(f"%{patient_name}%"))
       if(age):
           stmt = stmt.where(Patients.age>=age).order_by(Patients.age)
       if(family_id):
           stmt = stmt.where(Patients.family_id == family_id)
       if(insurance_id):
            stmt = stmt.where(Patients.insurance_id ==insurance_id)
       if(hmo_name):
            stmt = stmt.where(Patients.Insurance.name ==hmo_name)
       if(family_name):
        stmt = stmt.where(Patients.PatientFamily.name ==family_name)    
       result= db.execute(stmt).scalars().all()
       return result

def get_insurance(db:Session,hmo_id:PyUUID|None=None,hmo_name:str|None=None):
    if(hmo_id):
        try:
            stmt = select(Insurance).where(Insurance.id==hmo_id)
            hmo = db.execute(stmt).scalars().first()
            return hmo
        except:
            raise HTTPException(404,"HMO not Found")
    if(hmo_name):
        stmt = select(Insurance).where(Insurance.name.ilike(f"%{hmo_name}%"))
        hmo = db.execute(stmt).scalars().all()
        return hmo


    
def get_family(db:Session,family_id:PyUUID|None=None,family_name:str|None=None):
    if(family_id):
        try:
            stmt = select(PatientFamily).where(PatientFamily.id==family_id)
            family = db.execute(stmt).scalars().first()
            return family
        except:
            raise HTTPException(404,"Family not Found")
    if(family_name):
        stmt = select(PatientFamily).where(PatientFamily.name.ilike(f"%{family_name}%"))
        family = db.execute(stmt).scalars.all()
        return family



def db_add(db:Session,item:Patients):
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
        except:
            raise HTTPException(400,detail="Bad Request")


def db_delete(db:Session, item:Patients):
    try:
        db.delete(item)
        db.commit()
    except:
         raise HTTPException(404,detail="Item not Found")
    
    