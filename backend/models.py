from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID as PYUUID, uuid4
from schema import Roles


class Patients(Base):
    __tablename__ = 'patients'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    name: Mapped[str]
    age: Mapped[int]
    address: Mapped[str]
    phone: Mapped[str]
    picture_url:Mapped[str] = mapped_column(nullable=True)
    records :Mapped[list["Record"]] =  relationship(back_populates="patient")


    family_id:Mapped[PYUUID|None]=mapped_column(UUID(as_uuid=True), ForeignKey("family.id"),nullable=True)
    insurance_id:Mapped[PYUUID|None]=mapped_column(UUID(as_uuid=True), ForeignKey("insurance.id"),nullable=True)


    vitals:Mapped[list["Vitals"]]=relationship(back_populates="patient")
    insurance:Mapped["Insurance"]=relationship(back_populates="patient")
    family:Mapped["PatientFamily"]=relationship(back_populates="patient")


class Workers(Base):
    __tablename__ = 'workers'
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str] = mapped_column(unique=True)
    role:Mapped[Roles]
    hashed_password:Mapped[str]
    demerits:Mapped[int] = mapped_column(default=0)
    
    schedule:Mapped[list["Schedule"]] = relationship(back_populates="worker")
    vitals:Mapped[list["Vitals"]]=relationship(back_populates="worker")
    records:Mapped[list["Record"]]=relationship(back_populates="worker")
    permissions:Mapped[list["Permissions"]] = relationship(back_populates="worker")


class Schedule(Base):
    __tablename__ = 'schedule'
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    time:Mapped[datetime]
    worker_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),ForeignKey("workers.id"))

    worker:Mapped["Workers"] = relationship(back_populates="schedule")

class Pharmacy(Base):
    __tablename__="pharmacy"
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    drug_name:Mapped[str]
    batch_number:Mapped[int]
    quantity:Mapped[int]


    usage:Mapped[list[DrugsUsed]] = relationship(back_populates="pharmacy")



class Record(Base):
    __tablename__="records"
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    date:Mapped[datetime]
    diagnosis:Mapped[str]


    worker_id :Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),ForeignKey("workers.id"))
    patient_id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),ForeignKey("patients.id"))
    vitals_id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True), ForeignKey("vitals.id"),nullable=True)


    patient :Mapped["Patients"] =  relationship(back_populates="records")
    worker :Mapped["Workers"] =  relationship(back_populates="records")
    vitals:Mapped[Vitals]= relationship(back_populates="record")
    drugs:Mapped[list["DrugsUsed"]] = relationship(back_populates="record") 


class DrugsUsed(Base):
    __tablename__ = "drugs_used"
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    quantity:Mapped[int]
    drug_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),ForeignKey("pharmacy.id"))
    record_id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True), ForeignKey("records.id"))
    date:Mapped[datetime]

    pharmacy:Mapped["Pharmacy"]= relationship(back_populates="usage")
    record:Mapped["Record"] = relationship(back_populates="drugs")

class Vitals(Base):
    __tablename__ ="vitals"
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    temp:Mapped[float]
    heart:Mapped[float]
    pressure:Mapped[str]
    date:Mapped[datetime]
    
    worker_id :Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),ForeignKey("workers.id"))
    patient_id :Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),ForeignKey("patients.id"))

    worker: Mapped["Workers"] = relationship(back_populates="vitals")
    patient: Mapped["Patients"] = relationship(back_populates="vitals")
    record:Mapped[Record] = relationship(back_populates="vitals")


class Insurance(Base):
    __tablename__="insurance"
    id:Mapped[PYUUID]=mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str]

    patient:Mapped[list["Patients"]]=relationship(back_populates="insurance")


class PatientFamily(Base):
    __tablename__ = "family"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    name:Mapped[str] 

    patient:Mapped[list["Patients"]]=relationship(back_populates="family")


class Permissions(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    role:Mapped[str] = mapped_column(ForeignKey("workers.role"))
    perm:Mapped[str]

    worker:Mapped["Workers"] = relationship(back_populates="permissions")