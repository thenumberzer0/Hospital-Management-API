from models import DrugMaster, DrugsUsed, Batches,DrugType,DrugGroup,Location,Supplier,OtherDrugHistory,Inventory,DrugTransferHistory
from fastapi import HTTPException
from schema.pharmacy_schema import create_pharmacy_items,create_batches,create_drugs_used,create_drug_group,create_drug_type,create_drugs_other_used,create_locations,create_suppliers,update_pharmacy_items, transfer_drugs
from sqlalchemy.orm import Session
from uuid import UUID as PyUUID
from repos.pharmacy_repo import db_add, db_delete, drug_history,drug_other_history, db_batch_search, db_pharm_search,search_drug_group,search_drug_type,search_location,search_supplier,db_inventory_search



def update(updates,changed):
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(changed, key, value)
#drug group and type---------------------------------------------------------



def create_drug_group(db:Session,new_group:create_drug_group):
    drug_group = DrugGroup(name=new_group.name)
    db_add(db, drug_group)
    return {"Message": "New Drug Group Added", "id": drug_group.id}
def get_drug_group(db:Session,group_id:PyUUID|None=None):
    return search_drug_group(db,group_id)
def update_drug_group(db:Session,updates:create_drug_group,group_id:PyUUID):
    changed_group = search_drug_group(db,group_id)
    update(updates,changed_group)
    db_add(db, changed_group)
    return {"Message": "Drug Group updated"}
def delete_drug_group(db:Session,group_id:PyUUID):
    changed_group = search_drug_group(db,group_id)
    db_delete(changed_group)
    return {"Message":"Drug Group Deleted"}





def create_drug_type(db:Session,new_type:create_drug_type):
    drug_type = DrugType(name=new_type.name)
    db_add(db, drug_type)
    return {"Message": "New Drug Type Added", "id": drug_type.id}
def get_drug_type(db:Session,type_id:PyUUID|None=None):
    return search_drug_type(db,type_id)
def update_drug_type(db:Session,updates:create_drug_type,type_id:PyUUID):
    changed_type = search_drug_type(db,type_id)
    update(updates,changed_type)
    db_add(db, changed_type)
    return {"Message": "Drug type updated"}
def delete_drug_type(db:Session,type_id:PyUUID):
    changed_type = search_drug_group(db,type_id)
    db_delete(changed_type)
    return {"Message":"Drug type Deleted"}



# locations -----------
def create_location(db:Session,new_location:create_locations):
    location = Location(
        name = new_location.location_name
    )
    db_add(db, location)
    return {"Message": "New Location Added", "id": location.id}
def get_location(db:Session,location_id:PyUUID|None=None):
    return search_location(db,location_id)
def update_location(db:Session,update_location:create_locations,location_id:PyUUID):
    changed_location = search_location(db,location_id)  
    update(update_location,changed_location)
    db_add(db,changed_location)
    return {"Message":"Location Updated"}
def delete_location(db:Session,location_id:PyUUID):
    changed_location = search_location(db,location_id)
    db_delete(db,changed_location)
    return {"Message":"Location Updated"}

# supplier -----------
def create_supplier(db:Session,new_supplier:create_suppliers):
    supplier = Supplier(
        name = new_supplier.name
    )
    db_add(db, supplier)
    return {"Message": "New supplier Added", "id": supplier.id}
def get_supplier(db:Session,supplier_id:PyUUID|None=None):
    return search_supplier(db,supplier_id)
def update_supplier(db:Session,update_supplier1:create_suppliers,supplier_id:PyUUID):
    changed_supplier = search_supplier(db,supplier_id)  
    update(update_supplier1,changed_supplier)
    db_add(db, changed_supplier)
    return {"Message":"supplier Updated"}
def delete_supplier(db:Session,supplier_id:PyUUID):
    changed_supplier = search_supplier(db,supplier_id)
    db_delete(db,changed_supplier)
    return {"Message":"supplier Updated"}


# regular drugs---------------------------------------------------------


def get_drugs(db: Session, drug_name: str | None = None, drug_id: PyUUID | None = None, batch_no: int | None = None):
    return db_pharm_search(db, drug_name, drug_id, batch_no)


def create_drugs(db: Session, new_drug: create_pharmacy_items):
    drug = DrugMaster(name=new_drug.name,
                      drug_code=new_drug.drug_code
                      ,drug_groupid=new_drug.drug_groupid)
    db_add(db, drug)
    return {"Message": "New Drug Added", "id": drug.id}


def update_drug(db: Session, drug_id: PyUUID, updates: update_pharmacy_items):
    changed_drug = db_pharm_search(db, drug_id=drug_id)
    update(updates,changed_drug)
    db_add(db, changed_drug)
    return {"Message": "Drug Updated!", "name": changed_drug.name}


def delete_drug(db: Session, drug_id: PyUUID):
    changed_drug = db_pharm_search(db, drug_id=drug_id)
    db_delete(db, changed_drug)
    return {"Message": "Drug Deleted", "id": changed_drug.id, "name": changed_drug.name}


# batches----------------------------------------------------------------------

def get_batch(db: Session, drug_name: str | None = None, drug_id: PyUUID | None = None, batch_id: PyUUID | None = None):
    return db_batch_search(db, drug_name, drug_id, batch_id)

def create_batch(db: Session, new_batch: create_batches):
    batch = Batches(
        bulk_quantity = new_batch.bulk_quantity,
        conversion_rate=new_batch.conversion_rate,
        alert_level=new_batch.alert_level,
        batch_number=new_batch.batch_number,
        expiry_date=new_batch.expiry_date,
        pharmacy_id=new_batch.pharmacy_id,
        supplier_id = new_batch.supplier_id,
        location_id = new_batch.location_id,
        drug_group_id = new_batch.drug_group_id
    )
    inventory=Inventory(
        quantity = new_batch.conversion_rate * new_batch.bulk_quantity,
        location_id = new_batch.location_id,
        batch_id= batch.id
    )

    db_add(db, batch)
    db_add(db,inventory)
    return {"Message": "New Batch Added", "id": batch.id}


def delete_batch(db: Session, batch_id: PyUUID):
    changed_batch = db_batch_search(db, batch_id=batch_id)
    db_delete(db, changed_batch)
    return {"Message": "Batch Deleted", "id": changed_batch.id, "drug_name": changed_batch.pharmacy.name}


# used drugs (DrugsUsed)----------------------------------------------------------------------


def get_used_drugs(db: Session, batch_id: PyUUID | None = None,record_id: PyUUID | None = None,user_id: PyUUID | None = None,usage_id: PyUUID | None = None):
    return drug_history(db,batch_id, record_id,user_id,usage_id)


def create_used_drugs(db: Session, drug_used: create_drugs_used):
    inventory = db_inventory_search(db, inventory_id=drug_used.inventory_id)
    new_quantity = inventory.quantity - drug_used.quantity
    if new_quantity < 0:
        raise HTTPException(400, "Not enough stock in this batch")
    inventory.quantity = new_quantity

    used_drug = DrugsUsed(
        quantity=drug_used.quantity,
        inventory_id=inventory.id,
        date=drug_used.date,
        record_id=drug_used.record_id
    )
    db_add(db, inventory)
    db_add(db, used_drug)
    return {"Message": f"Drug used: {inventory.batch.pharmacy.name}", "quantity": used_drug.quantity, "id": used_drug.id}



def delete_used_drug(db: Session, usage_id: PyUUID):
    drug_usage = drug_history(db, usage_id)
    inventory = drug_usage.inventory
    inventory.quantity += drug_usage.quantity
    db_add(db, inventory)
    db_delete(db, drug_usage)
    return {"Message": "Usage Deleted"}

#Used other drug ----------------------------------------------------------------------




def get_other_used_drugs(db: Session, inventory_id: PyUUID | None = None, usage_id: PyUUID | None = None):
    return drug_other_history(db, inventory_id,usage_id)


def create_other_used_drugs(db: Session, other_drug_used: create_drugs_other_used,worker_id):
    inventory = db_inventory_search(db, inventory_id=other_drug_used.inventory_id)
    new_quantity = inventory.quantity - other_drug_used.quantity
    if new_quantity < 0:
        raise HTTPException(400, "Not enough stock in this batch")
    used_drug = OtherDrugHistory(
        quantity=other_drug_used.quantity,
        inventory_id=inventory.id,
        date=other_drug_used.date,
        memo=other_drug_used.memo,
        worker_id = worker_id
    )
    db_add(db, inventory)
    db_add(db, used_drug)
    return {"Message": f"Drug used: {inventory.batch.pharmacy.name}", "quantity": other_drug_used.quantity, "id": used_drug.id}




def delete_other_used_drug(db: Session, usage_id: PyUUID):
    drug_usage = drug_other_history(db, usage_id)
    inventory = drug_usage.inventory
    inventory.quantity += drug_usage.quantity
    db_add(db, inventory)
    db_delete(db, drug_usage)
    return {"Message": "Usage Deleted"}

#Inventory 
def get_inventory(db: Session,inventory_id:PyUUID|None=None,location_id:PyUUID|None=None,batch_id:PyUUID|None=None):
    return db_inventory_search(db,inventory_id,location_id,batch_id)


#SOME SPECIAL SERVICES IG
def inventory_location_transfer(db:Session,transfer_details:transfer_drugs,workerid:PyUUID):
    location = search_location(db,transfer_details.new_location_id)
    if not location:
        raise HTTPException(404,"Location Not Found")
    inventory = db_inventory_search(db,inventory_id=transfer_details.inventory_id)
    if not inventory:
            raise HTTPException(404,"Location Not Found")
    final_quantity = inventory.quantity - transfer_details.new_quantity
    if final_quantity<0:
        raise HTTPException(400,"Quantity too high")
    update({"quantity":final_quantity},inventory)
    new_inventory = Inventory(
        quantity = transfer_details.new_quantity,
        location_id = transfer_details.new_location_id,
        batch_id= inventory.batch_id
    )
    
    history = DrugTransferHistory(
        quantity = transfer_details.new_quantity,
        old_location_id = inventory.location_id,
        new_location_id = transfer_details.new_location_id,
        batch_id = inventory.batch_id,
        worker_id = workerid,
        date = transfer_details.date
    )
    db_add(db, inventory)
    db_add(db,new_inventory)

    
    
    