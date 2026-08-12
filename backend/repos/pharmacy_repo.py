from sqlalchemy.orm import Session
from models import Pharmacy, DrugsUsed, Patients, Record
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID as PyUUID
from sqlalchemy import text, select


def db_search(db:Session,drug_name:str|None=None,drug_id:PyUUID|None =None,batch_no:int|None=None):
       if(drug_id):
        try:
            stmt = db.query(Pharmacy).where(Pharmacy.id==drug_id).first()
            drug = db.execute(stmt).scalars().first()
        except:
            raise HTTPException(404,"Item not Found")
       return drug
       stmt = """SELECT * FROM PHARMACY"""
       result= db.execute(text(stmt)).scalars().all()
       drugs=result
    
       if(drug_name):
           drugs = [u for u in drug if u.name == drug_name]
       if(batch_no):
           drugs = [u for u in drug if u.batch_no == batch_no]
       return drugs


#show particular  used of a 
def drug_history(db:Session, drug_id:PyUUID|None = None, user_id:PyUUID|None = None,user_name:str|None=None):
    stmt = select(Pharmacy.drug_name,Pharmacy.id,DrugsUsed.quantity,Patients.name,Patients.id.label("user_id")).join(DrugsUsed).join(Record).join(Patients).order_by(Pharmacy.usage.date)
    result = db.execute(stmt).mappings().all()
    if(drug_id):
        for i in result:
            result = [u for u in result if u.id==drug_id]
        return result
    if(user_id):
        for i in result:
            result = [u for u in result if u.user_id==user_id]
        return result
    return result



def db_add(db:Session,item:Pharmacy|DrugsUsed):
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
        except:
            raise HTTPException(400,detail="Bad Request")


def db_delete(db:Session, item:Pharmacy|DrugsUsed):
    try:
        db.delete(item)
        db.commit()
    except:
         raise HTTPException(404,detail="Item not Found")
    
    