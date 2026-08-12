from fastapi import Depends,APIRouter, HTTPException, status
from database import get_db
from schema import create_pharmacy_items,drugs_used_create, update_pharmacy_item
from sqlalchemy.orm import Session
from dependencies import get_currentUser
from uuid import UUID as PyUUID
import services.pharmacy_services as pharmacy_services

pharmacy_router = APIRouter()
#regular drugs
@pharmacy_router.get("/",status_code=status.HTTP_200_OK)
def get_drugs(db:Session=Depends(get_db),drug_name:str|None=None,drug_id:PyUUID|None =None,batch_no:int|None=None):
   return pharmacy_services.get_drugs(db,drug_name,drug_id,batch_no)

@pharmacy_router.post("/",status_code=status.HTTP_202_ACCEPTED)
def create_drugs(new_drug:create_pharmacy_items,db:Session=Depends(get_db)):
    pharmacy_services.create_drugs(db,new_drug)

@pharmacy_router.patch("/",status_code=status.HTTP_202_ACCEPTED)
def update_drug(drug_id:PyUUID,updates:update_pharmacy_item,db:Session=Depends(get_db)):
    pharmacy_services.update_drug(drug_id,updates,db)
    
@pharmacy_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def delete_drug(drug_id:PyUUID,db:Session=Depends(get_db)):
    pharmacy_services.delete_drug(db,drug_id)

#used drugs services

@pharmacy_router.get("/u",status_code=status.HTTP_200_OK)
def get_used_drugs(db:Session=Depends(get_db), drug_id:PyUUID|None = None, user_id:PyUUID|None = None,user_name:str|None=None):
    return pharmacy_services.get_used_drugs(db,drug_id,user_id,user_name)

@pharmacy_router.post("/u",status_code=status.HTTP_202_ACCEPTED)
def create_used_drugs(drug_used:drugs_used_create,db:Session=Depends(get_db)):
   pharmacy_services.create_used_drugs(db,drug_used)

@pharmacy_router.patch("/u",status_code=status.HTTP_202_ACCEPTED)
def update_used_drug(pharmacy_id:PyUUID, drug_used_id:PyUUID,new_quantity:int,db:Session=Depends(get_db)):
   pharmacy_services.update_used_drug(db,pharmacy_id,drug_used_id,new_quantity)

@pharmacy_router.delete("/u",status_code=status.HTTP_204_NO_CONTENT)
def delete_used_drug(pharmacy_id:PyUUID, drug_used_id:PyUUID,db:Session=Depends(get_db)):
   pharmacy_services.delete_used_drug(db,pharmacy_id,drug_used_id)