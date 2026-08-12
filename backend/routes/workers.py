from fastapi import Depends,APIRouter, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from dependencies import get_currentUser
from schema import create_workers,update_workers,create_vitals,create_records, schedule_manage, login_worker,schedule_update
from uuid import UUID as PyUUID
import services.workers_services as worker_services 
from datetime import datetime
worker_router = APIRouter()

@worker_router.post("/login",status_code=status.HTTP_202_ACCEPTED)
def login_users(worker:login_worker,db:Session=Depends(get_db)):
    return worker_services.login_user(db,user=worker)

@worker_router.post("/",status_code=status.HTTP_201_CREATED)
def create_workers(worker:create_workers,db:Session=Depends(get_db)):
    worker_services.create_workers(db,worker)


@worker_router.get("/",status_code=status.HTTP_200_OK)
def get_workers(db:Session=Depends(get_db),worker_id:PyUUID|None=None,worker_name:str|None=None,role:str|None=None,currentUser = Depends(get_currentUser)):
    return worker_services.get_workers(db,worker_id,worker_name,role)

@worker_router.patch("/",status_code=status.HTTP_202_ACCEPTED)
def update_worker(worker_id:PyUUID,updates:update_workers,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.update_worker(db,worker_id,updates)

@worker_router.delete("/",status_code=status.HTTP_204_NO_CONTENT)
def delete_worker(worker_id:PyUUID,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.delete_worker(db,worker_id)






@worker_router.post("/vitals",status_code=status.HTTP_202_ACCEPTED)
def submit_vitals(work:create_vitals,currentUser = Depends(get_currentUser),db:Session=Depends(get_db)):
    worker_services.submit_vitals(db,work,currentUser.id)

@worker_router.post("/records",status_code=status.HTTP_202_ACCEPTED)
def submit_Records(user:PyUUID,work:create_records,vitals_id:PyUUID,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.submit_Records(db,currentUser.id,work,vitals_id)

@worker_router.get("/work",status_code=status.HTTP_200_OK)
def retrieve_work(worker_id:PyUUID,db:Session=Depends(get_db)):
    return worker_services.get_worker_Work(db,worker_id)

@worker_router.delete("/work",status_code=status.HTTP_204_NO_CONTENT)
def delete_work(work_id:PyUUID,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.delete_work(db,work_id)
            





@worker_router.post("/schedule",status_code=status.HTTP_202_ACCEPTED)
def create_schedule(schedule:schedule_manage,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.create_schedule(db,schedule)

@worker_router.get("/schedule",status_code=status.HTTP_200_OK)  
def get_schedule(db:Session=Depends(get_db),currentUser = Depends(get_currentUser),worker_id:PyUUID|None=None,time:datetime|None=None,schedule_id:PyUUID|None=None):
    return worker_services.get_schedule(db,worker_id,time,schedule_id)
    
@worker_router.patch("/schedule",status_code=status.HTTP_202_ACCEPTED)
def update_schedule(schedule_id:PyUUID, updates:schedule_update,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
    worker_services.update_schedule(db,schedule_id,updates)

@worker_router.delete("/schedule",status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id:PyUUID,db:Session=Depends(get_db),currentUser = Depends(get_currentUser)):
     worker_services.delete_schedule(db,schedule_id)

