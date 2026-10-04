from sqlalchemy.orm import Session
from models  import DrugMaster, DrugsUsed, Batches, Record,OtherDrugHistory, DrugGroup,DrugType,Supplier,Location, Inventory, DrugTransferHistory
from fastapi import HTTPException
from uuid import UUID as PyUUID
from sqlalchemy import select





def db_inventory_search(db: Session,inventory_id:PyUUID|None=None,location_id:PyUUID|None=None,batch_id:PyUUID|None=None):
    if inventory_id:
        inventory = db.execute(select(Inventory).where(Inventory.id == inventory_id)).scalars().first()
        if not inventory:
                raise HTTPException(404, "Item not Found")
        return inventory
    
    stmt = select(Inventory)
    if(batch_id):
        stmt = stmt.where(Inventory.batch_id==batch_id)
    if(location_id):
        stmt = stmt.where(Inventory.location_id==location_id)
    return db.execute(stmt).scalars().all()

def db_pharm_search(db: Session, drug_name: str | None = None, drug_id: PyUUID | None = None, batch_no: int | None = None):
    if drug_id:
        drug = db.execute(select(DrugMaster).where(DrugMaster.id == drug_id)).scalars().first()
        if not drug:
            raise HTTPException(404, "Item not Found")
        return drug
    stmt = select(DrugMaster)
    if drug_name:
        stmt = stmt.where(DrugMaster.name.ilike(f"%{drug_name}%"))
    return db.execute(stmt).scalars().all()


def db_batch_search(db: Session, drug_name: str | None = None, drug_id: PyUUID | None = None, batch_id: PyUUID | None = None):
    if batch_id:
        batch = db.execute(select(Batches).where(Batches.id == batch_id)).scalars().first()
        if not batch:
            raise HTTPException(404, "Item not Found")
        return batch

    stmt = select(Batches,DrugMaster)
    if drug_id:
        stmt = stmt.where(Batches.drug_id == drug_id)
    if drug_name:
        stmt = stmt.where(Batches.pharmacy.has(DrugMaster.name.ilike(f"%{drug_name}%")))

    stmt = stmt.order_by(Batches.expiry_date.asc(), Batches.quantity.asc())
    return db.execute(stmt).mappings().all()



def drug_history(db: Session, inventory_id: PyUUID | None = None,record_id: PyUUID| None = None, user_id: PyUUID | None = None, usage_id: PyUUID | None = None):
    if usage_id:
        used = db.execute(select(DrugsUsed).where(DrugsUsed.id == usage_id)).scalars().first()
        if not used:
            raise HTTPException(404, "Item not Found")
        return used

    stmt = select(DrugsUsed)
    if inventory_id:
        stmt = stmt.where(DrugsUsed.batch_id == inventory_id)
    if record_id:
        stmt = stmt.where(DrugsUsed.record_id == record_id)
    if user_id:
        stmt = stmt.where(DrugsUsed.record.has(Record.patient_id == user_id))
    return db.execute(stmt).scalars().all()



def drug_other_history(db: Session, inventory_id: PyUUID | None = None, usage_id: PyUUID | None = None):
    if usage_id:
        used = db.execute(select(OtherDrugHistory).where(OtherDrugHistory.id == usage_id)).scalars().first()
        if not used:
            raise HTTPException(404, "Item not Found")
        return used
    
    stmt = select(OtherDrugHistory)
    if inventory_id:
        stmt = stmt.where(OtherDrugHistory.inventory_id == inventory_id)
    return db.execute(stmt).scalars().all()


def search_drug_group(db:Session,group_id:PyUUID|None=None):
    if(group_id):
        group = db.execute(select(DrugGroup).where(DrugGroup.id==group_id)).scalars().first()
        if not group:
            raise HTTPException(404, "Item not Found")
        return group
    
    stmt = select(DrugGroup)
    group=db.execute(stmt).scalars().all()
    return group


def search_drug_type(db:Session,type_id:PyUUID|None=None):
    if(type_id):
        type = db.execute(select(DrugType).where(DrugType.id==type_id)).scalars().first()
        if not type:
            raise HTTPException(404, "Item not Found")
        return type
    stmt = select(DrugType)
    type=db.execute(stmt).scalars().all()
    return type

def search_supplier(db:Session,supplier_id:PyUUID|None=None):
    if(supplier_id):
        supplier = db.execute(select(Supplier).where(Supplier.id==supplier_id)).scalars().first()
        if not supplier:
            raise HTTPException(404, "Item not Found")
        return supplier
    stmt= select(Supplier)
    suppliers = db.execute(stmt).scalars().all()
    return suppliers

def search_location(db:Session,location_id:PyUUID|None=None):
    if(location_id):
        location = db.execute(select(Location).where(Location.id==location_id)).scalars().first()
        if not location:
            raise HTTPException(404, "Item not Found")
        return location
    stmt= select(Location)
    locations = db.execute(stmt).scalars().all()
    return locations

    
    
def db_add(db: Session, item: DrugMaster | DrugsUsed | Batches|OtherDrugHistory|DrugType|DrugGroup|Inventory|DrugTransferHistory):
    try:
        db.add(item)
        db.commit()
        db.refresh(item)
    except Exception:
        db.rollback()
        raise HTTPException(400, detail="Bad Request")
    return item


def db_delete(db: Session, item: DrugMaster | DrugsUsed | Batches|OtherDrugHistory|DrugType|DrugGroup|Inventory):
    try:
        db.delete(item)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(404, detail="Item not Found")
