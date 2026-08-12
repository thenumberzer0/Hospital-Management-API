from repos.workers_repo import db_add,db_delete, db_search,get_worker_Work, gamble_workSearch,get_aschedule
from models import Workers, Record, Vitals, Schedule
from fastapi import HTTPException
from auth import hash_password, verify_password, create_access_token
from schema import create_workers,update_workers,create_vitals,create_records, schedule_manage, login_worker,schedule_update
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID as PyUUID
from auth import hash_password
from datetime import datetime
#be able to create or edit workers and possible delete
#show things they're responsible for
#make them able to drop things they're responsible for

def create_workers(db:Session,worker:create_workers):
    new_worker=Workers(
        name = worker.name,
        role=worker.role,
        hashed_password =hash_password(worker.password)
    )
    db_add(db,new_worker)
    return {"Message":"New Worker Made Successfully"}

def login_user(db:Session,user:login_worker):
    for i in db_search(db,worker_name=user.name):
        sus_user = i


    if(verify_password(user.password,sus_user.hashed_password)):
        user_permissions = sus_user.permissions
        token_jwtt=create_access_token(data={"user_id":str(sus_user.id),"permissions":user_permissions})
        return {"access_token":token_jwtt}
    else:
        raise HTTPException(401,"Wrong Credentials")


def get_workers(db:Session,worker_id:PyUUID|None=None,worker_name:str|None=None,role:str|None=None):
    return db_search(db,worker_id,worker_name,role)
    

def update_worker(db:Session,worker_id:PyUUID,updates:update_workers):
    updates = updates.model_dump(exclude_unset=True)
    try:
        stmt = select(Workers).where(Workers.id==worker_id)
        changed_user = db.execute(stmt).scalars().first()
    except:
        raise HTTPException(404,"User not Found")
    for key, value in updates.items():
        setattr(changed_user, key, value)

    db_add(db,changed_user)
    return{"Message":"Worker Updated!"}

def delete_worker(db:Session,worker_id:PyUUID):
    try:
        stmt = select(Workers).where(Workers.id==worker_id)
        changed_user = db.execute(stmt).scalars().first()
    except:
        raise HTTPException(404,"User not Found")
    db_delete(db, changed_user)
    return{"Message":"User Deleted Successfully"}








def submit_vitals(db:Session,work:create_vitals,user:PyUUID):
    vitals = Vitals(
        temp= work.temp,
        heart=work.heart,
        pressure = work.pressure,
        date = work.date,
        worker_id =  user,
        patient_id = work.patient_id
    )
    db_add(db,vitals)
    return{"Vitals uploaded":vitals.id}

def submit_Records(db:Session,user:PyUUID,work:create_records,vitals_id:PyUUID):
    record = Record(
        date = work.date,
        diagnosis = work.diagnosis,
        worker_id = user,
        patient_id = work.patient_id,
        vitals_id = vitals_id
    )
    db_add(db,record)
    return{"Record Uploaded":record.id}


def retrieve_work(db:Session,worker_id:PyUUID):
    return get_worker_Work(db,worker_id)


def delete_work(db:Session,work_id:PyUUID):
    work = gamble_workSearch(db,work_id)
    db_delete(db, work)
    return {"Job deleted":work.id}
          

def create_schedule(db:Session, schedule:schedule_manage):
    new_schedule = Schedule(
        time=schedule.time,
        worker_id=schedule.worker_id
    )
    db_add(db,new_schedule)
    return{"Message":"Schedule Created!"}

def get_schedule(db:Session, worker_id:PyUUID|None=None,time:datetime|None=None,schedule_id:PyUUID|None=None):
    return get_aschedule(db,worker_id,time,schedule_id)


def update_schedule(db:Session,schedule_id:PyUUID, updates:schedule_update):
    updates = updates.model_dump(exclude_unset=True)
    result = get_schedule(db,schedule_id=schedule_id)
    for key, value in updates.items():
            setattr(result, key, value)
    db_add(db,result)
    return{"Message":"Worker Schedule Updated!"}



def delete_schedule(db:Session,schedule_id:PyUUID):
     result = get_schedule(db,schedule_id=schedule_id)
     db_delete(db,result)
     return{"Message":"Schedule Deleted!"}