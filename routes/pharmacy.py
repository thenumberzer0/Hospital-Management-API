from fastapi import Depends, APIRouter, status
from database import get_db
from schema.pharmacy_schema import create_pharmacy_items,create_batches,create_drugs_used,create_drug_group,create_drug_type,create_drugs_other_used,create_locations,create_suppliers,update_pharmacy_items, transfer_drugs
from sqlalchemy.orm import Session
from dependencies import get_currentUser,require_permissions
from uuid import UUID as PyUUID
import services.pharmacy_services as pharmacy_services

pharmacy_router = APIRouter()

# regular drugs


@pharmacy_router.get("/", status_code=status.HTTP_200_OK)
def get_drugs(db: Session = Depends(get_db), drug_name: str | None = None, drug_id: PyUUID | None = None,
              batch_no: int | None = None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_drugs(db, drug_name, drug_id, batch_no)


@pharmacy_router.post("/", status_code=status.HTTP_202_ACCEPTED)
def create_drugs(new_drug: create_pharmacy_items, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["drugs.create"]))):
    return pharmacy_services.create_drugs(db, new_drug)


@pharmacy_router.patch("/", status_code=status.HTTP_202_ACCEPTED)
def update_drug(drug_id: PyUUID, updates: update_pharmacy_items, db: Session = Depends(get_db),
                 currentUser=Depends(require_permissions(["drugs.update"]))):
    return pharmacy_services.update_drug(db, drug_id, updates)


@pharmacy_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug(drug_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["drugs.delete"]))):
    pharmacy_services.delete_drug(db, drug_id)

########group

@pharmacy_router.get("/group", status_code=status.HTTP_200_OK)
def get_drug_group(db: Session = Depends(get_db),group_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_drug_group(db,group_id)

@pharmacy_router.post("/group", status_code=status.HTTP_202_ACCEPTED)
def create_drug_groupf(new_group:create_drug_group,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_g.create"]))):
    pharmacy_services.create_drug_group(db,new_group)

@pharmacy_router.patch("/group", status_code=status.HTTP_202_ACCEPTED)
def update_drug_group(updates:create_drug_group,group_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_g.update"]))):
    pharmacy_services.update_drug_group(db,updates,group_id)

@pharmacy_router.delete("/group", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug_group(group_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_g.delete"]))):
    pharmacy_services.delete_drug_group(db,group_id)



########type
@pharmacy_router.get("/type", status_code=status.HTTP_200_OK)
def get_drug_type(db: Session = Depends(get_db),type_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_drug_type(db,type_id)

@pharmacy_router.post("/type", status_code=status.HTTP_202_ACCEPTED)
def create_drug_typef(new_type:create_drug_type,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_t.create"]))):
    pharmacy_services.create_drug_type(db,new_type)

@pharmacy_router.patch("/type", status_code=status.HTTP_202_ACCEPTED)
def update_drug_type(updates:create_drug_type,type_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_t.update"]))):
    pharmacy_services.update_drug_type(db,updates,type_id)

@pharmacy_router.delete("/type", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug_type(type_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug_t.delete"]))):
    pharmacy_services.delete_drug_type(db,type_id)


# location #############################################
@pharmacy_router.get("/location", status_code=status.HTTP_200_OK)
def get_location(db: Session = Depends(get_db),location_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_location(db,location_id)

@pharmacy_router.post("/location", status_code=status.HTTP_202_ACCEPTED)
def create_drug_location(new_location:create_locations,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["location.create"]))):
    pharmacy_services.create_location(db,new_location)

@pharmacy_router.patch("/location", status_code=status.HTTP_202_ACCEPTED)
def update_location(updates:create_locations,location_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["location.update"]))):
    pharmacy_services.update_location(db,updates,location_id)

@pharmacy_router.delete("/location", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(location_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["location.delete"]))):
    pharmacy_services.delete_location(db,location_id)

# supplier #############################################
@pharmacy_router.get("/supplier", status_code=status.HTTP_200_OK)
def get_supplier(db: Session = Depends(get_db),supplier_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_supplier(db,supplier_id)

@pharmacy_router.post("/supplier", status_code=status.HTTP_202_ACCEPTED)
def create_supplier(new_supplier:create_suppliers,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["supplier.create"]))):
    pharmacy_services.create_supplier(db,new_supplier)

@pharmacy_router.patch("/supplier", status_code=status.HTTP_202_ACCEPTED)
def update_supplier(updates:create_suppliers,supplier_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["supplier.update"]))):
    pharmacy_services.update_supplier(db,updates,supplier_id)

@pharmacy_router.delete("/supplier", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id:PyUUID,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["supplier.delete"]))):
    pharmacy_services.delete_supplier(db,supplier_id)



#####################batches

@pharmacy_router.get("/batch", status_code=status.HTTP_200_OK)
def get_batches(db: Session = Depends(get_db), drug_name: str | None = None, drug_id: PyUUID | None = None,
                 batch_id: PyUUID | None = None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_batch(db, drug_name, drug_id, batch_id)


@pharmacy_router.post("/batch", status_code=status.HTTP_202_ACCEPTED)
def create_batch(new_batch: create_batches, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["batch.create"]))):
    return pharmacy_services.create_batch(db, new_batch)


@pharmacy_router.delete("/batch", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch(batch_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["batch.delete"]))):
    pharmacy_services.delete_batch(db, batch_id)


# used drugs

@pharmacy_router.get("/u", status_code=status.HTTP_200_OK)
def get_used_drugs(db: Session = Depends(get_db), inventory_id: PyUUID | None = None, user_id: PyUUID | None = None,record_id: PyUUID | None = None, usage_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_used_drugs(db, inventory_id,record_id, user_id,usage_id)


@pharmacy_router.post("/u", status_code=status.HTTP_202_ACCEPTED)
def create_used_drugs(drug_used: create_drugs_used, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["drug_u.create"]))):
    return pharmacy_services.create_used_drugs(db, drug_used)


@pharmacy_router.delete("/u", status_code=status.HTTP_204_NO_CONTENT)
def delete_used_drug(usage_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(require_permissions(["drug_u.delete"]))):
    pharmacy_services.delete_used_drug(db, usage_id)

#other used



@pharmacy_router.get("/ou", status_code=status.HTTP_200_OK)
def get_other_used_drugs(db: Session = Depends(get_db), inventory_id: PyUUID | None = None, usage_id: PyUUID | None = None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_other_used_drugs(db, inventory_id,usage_id)


@pharmacy_router.post("/ou", status_code=status.HTTP_202_ACCEPTED)
def create_other_used_drugs(other_drug_used: create_drugs_other_used, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    return pharmacy_services.create_other_used_drugs(db, other_drug_used,currentUser.id)



@pharmacy_router.delete("/ou", status_code=status.HTTP_204_NO_CONTENT)
def delete_other_used_drug(usage_id: PyUUID, db: Session = Depends(get_db), currentUser=Depends(get_currentUser)):
    pharmacy_services.delete_other_used_drug(db, usage_id)








@pharmacy_router.get("/inventory", status_code=status.HTTP_200_OK)
def get_inventory_items(db: Session = Depends(get_db), inventory_id:PyUUID|None=None,location_id:PyUUID|None=None,batch_id:PyUUID|None=None,currentUser=Depends(get_currentUser)):
    return pharmacy_services.get_inventory(db,inventory_id,location_id,batch_id)









@pharmacy_router.post("/transfer", status_code=status.HTTP_202_ACCEPTED)
def drug_transfer(transfer_details:transfer_drugs,db: Session = Depends(get_db),currentUser=Depends(require_permissions(["drug.transfer"]))):
    pharmacy_services.inventory_location_transfer(db,transfer_details,currentUser.id)