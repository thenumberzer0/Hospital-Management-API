from datetime import datetime
from uuid import UUID as PyUUID
from typing import Optional
from pydantic import BaseModel

class create_pharmacy_items(BaseModel):
    name: str
    drug_code: str

class update_pharmacy_items(BaseModel):
    name: Optional[str] = None
    drug_code:Optional[str]= None

class create_drug_group(BaseModel):
    name:str
class create_drug_type(BaseModel):
    name:str

class create_locations(BaseModel):
    location_name:str
class create_suppliers(BaseModel):
    name:str


   
class create_batches(BaseModel):
    bulk_quantity:int
    conversion_rate:int
    batch_number: str
    expiry_date: datetime
    supplier_id:PyUUID 
    location_id:PyUUID
    pharmacy_id: PyUUID
    drug_group_id:PyUUID

    
    
class update_batches(BaseModel):
    location_id:Optional[PyUUID] = None
    supplier_id:Optional[PyUUID] = None


class create_drugs_used(BaseModel):
    quantity: int
    date: datetime
    inventory_id: PyUUID
    record_id: PyUUID


class create_drugs_other_used(BaseModel):
    quantity: int
    memo:str
    date:datetime
    inventory_id:PyUUID

class transfer_loc_drugs(BaseModel):
    inventory_id:PyUUID
    new_location_id:PyUUID
    new_quantity:int
    date:datetime

class transfer_other_inventory(BaseModel):
    inventory_id:PyUUID
    other_invetory_id:PyUUID
    new_quantity:int
    date:datetime

    