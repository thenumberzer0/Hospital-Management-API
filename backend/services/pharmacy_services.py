from models import Pharmacy,DrugsUsed
from fastapi import HTTPException
from schema import create_pharmacy_items,drugs_used_create, update_pharmacy_item
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID as PyUUID
from repos.pharmacy_repo import db_add,db_delete, db_search, drug_history

#regular drugs
def get_drugs(db:Session,drug_name:str|None=None,drug_id:PyUUID|None =None,batch_no:int|None=None):
    return db_search(db,drug_name,drug_id,batch_no)

def create_drugs(db:Session,new_drug:create_pharmacy_items):
    drug=Pharmacy(
        drug_name = new_drug.name,
        quantity = new_drug.quantity,
        batch_number= new_drug.batch_number

    )
    db_add(db,drug)
    return {"Message":"New Drug Added"}

def update_drug(db:Session,drug_id:PyUUID,updates:update_pharmacy_item):
    changed_drug= db_search(db,drug_id=drug_id)
    updates = updates.model_dump(exclude_unset=True)
    for key, value in updates.items():
            setattr(changed_drug, key, value)
    db_add(db,changed_drug)
    return{"Drug Updated!":changed_drug.drug_name}

def delete_drug(db:Session,drug_id:PyUUID):
    changed_drug= db_search(db,drug_id=drug_id)
    db_delete(db, changed_drug)
    return{"Message":"Drug Deleted",changed_drug.id:changed_drug.drug_name}

#used drugs services

#in this im expecting drugs that belong to a particular user, that they used
def get_used_drugs(db:Session, drug_id:PyUUID|None = None, user_id:PyUUID|None = None,user_name:str|None=None):
    return drug_history(db,drug_id,user_id,user_name)

def create_used_drugs(db:Session, drug_used:drugs_used_create):
   drug = db_search(db,drug_id=drug_used.drug_id)
   new_quantity = drug.quantity-drug_used.quantity
   if(new_quantity>0):
        drug.quantity = new_quantity
   else:
       raise HTTPException(400,"Bad Request")
   used_drug = DrugsUsed(
       quantity= drug_used.quantity,
       drug_id = drug.id,
       date = drug_used.date,
       record_id = drug_used.record_id
   )
   db_add(db,drug)
   db_add(db,used_drug)
   return {f"Drug used {drug.drug_name}":used_drug.quantity}


def update_used_drug(db:Session,pharmacy_id:PyUUID, drug_used_id:PyUUID,new_quantity:int):
   drug = db_search(db,drug_id=pharmacy_id.drug_id)
   drug_usage = [u for u in drug.usage if u.id==drug_used_id][0]
   #drug = real drug, drug_usage = the specific usage item, 
   #so basically we're gonna change the quantity of usage to new quantity and compare it with only the past quantity
   #making sure drug+past - new is greater than zero
   final_quantity = (drug.quantity+drug_usage) - new_quantity
   #lets take d_uq = 7 then newq = 4  or basically we just add past to drug then minus new 
   if(final_quantity>0):
        drug_usage.quantity = new_quantity
        drug.quantity = final_quantity
        db_add(db,drug_usage)
        db_add(db,drug)
        return{"Message":"Updated Successfully",drug.drug_name:final_quantity}
   else:
       raise HTTPException(400,"Bad Request")

def delete_used_drug(db:Session,pharmacy_id:PyUUID, drug_used_id:PyUUID):
   drug = db_search(db,drug_id=pharmacy_id.drug_id)
   drug_usage = [u for u in drug.usage if u.id==drug_used_id][0]
   drug.quantity += drug_usage.quantity
   db_delete(db,drug_usage)
   return{"Message":"Usage Deleted"}
   