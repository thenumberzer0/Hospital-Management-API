from sqlalchemy.orm import Session
from models import Workers, Record, Vitals, Schedule
from fastapi import HTTPException
from sqlalchemy.dialects.postgresql import UUID as PyUUID
from sqlalchemy import select
from datetime import datetime


def db_add(db:Session,item:Workers|Record|Vitals|Schedule):
        try:
            db.add(item)
            db.commit()
            db.refresh(item)
        except:
            raise HTTPException(400,detail="Bad Request")

def db_delete(db:Session, item:Workers|Record|Vitals|Schedule):
    try:
        db.delete(item)
        db.commit()
    except:
         raise HTTPException(404,detail="Item not Found")
    
    
def db_search(db:Session,worker_id:PyUUID|None=None,worker_name:str|None=None,role:str|None=None):
       if(worker_id):
        try:
            stmt = select(Workers).where(Workers.id==worker_id)
            workers = db.execute(stmt).scalars().first()
            return workers
        except:
            raise HTTPException(404,"User not Found")
       stmt = select(Workers)
       
       if(worker_name):
           print(worker_name)
           stmt = stmt.where(Workers.name==worker_name)
       if(role):
           stmt = stmt.where(Workers.role==role)
       result= db.execute(stmt).scalars().all()
       worker=result
       return worker


def get_worker_Work(db:Session,worker_id:PyUUID):
        try:
            stmt = db.select(Workers).where(Workers.id==worker_id)
            worker = db.execute(stmt).scalars().all()
        except:
            raise HTTPException(404,"User not Found")
        if worker.role=="nurse":
            work = worker.vitals
        else:
            work = worker.records
        return work

def gamble_workSearch(db:Session, work_id):
    try:
        work = db.select(Vitals).where(Vitals.id==work_id)

        if not work:
            raise HTTPException(404,"Item not found")
    except HTTPException:
        try:
            work = db.select(Record).where(Record.id==work_id)
            if not work:
               raise HTTPException(404,"Item not found")
        except HTTPException: 
             raise HTTPException(404,"Item not found")
    return work






def get_aschedule(db:Session,worker_id:PyUUID|None=None,dt:datetime|None=None,schedule_id:PyUUID|None=None):
   stmt = select(Schedule)
   if(schedule_id):
        stmt = stmt.where(Schedule.id==schedule_id)
        schedules = db.execute(stmt).scalars().first()
        return schedules
   if(worker_id):
            stmt = stmt.where(Schedule.worker_id==worker_id)
   if(dt):
            stmt = stmt.where(Schedule.time==dt.day)
   schedules = db.execute(stmt).scalars().all()
   return schedules




