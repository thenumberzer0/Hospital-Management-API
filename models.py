from sqlalchemy import ForeignKey, Enum, CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID as PYUUID, uuid4
from schema.worker_schema import Roles, Gender


# -----------------------------------------------------------------------------------------------------
class Patients(Base):
    __tablename__ = 'patients'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(index=True)
    doB: Mapped[datetime]
    address: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str]= mapped_column(nullable=True)
    picture_url: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), default=datetime.utcnow)

    family_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("family.id", ondelete="SET NULL"), nullable=True)
    insurance_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("insurance.id", ondelete="SET NULL"), nullable=True)

    allergies: Mapped[list["SpecialDetails"]] = relationship(back_populates="patient")
    appointments: Mapped[list["Appointments"]] = relationship(back_populates="patients")
    records: Mapped[list["Record"]] = relationship(back_populates="patient")
    vitals: Mapped[list["Vitals"]] = relationship(back_populates="patient")
    insurance: Mapped["Insurance"] = relationship(back_populates="patients")
    family: Mapped["PatientFamily"] = relationship(back_populates="patients")


class SpecialDetails(Base):
    __tablename__ = 'special_details'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="CASCADE"))
    notes: Mapped[str]

    patient: Mapped["Patients"] = relationship(back_populates="allergies")


class Appointments(Base):
    __tablename__ = 'appointments'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    patient_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="RESTRICT"))
    day_time: Mapped[datetime]
    notes:Mapped[str]
    worker_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="SET NULL"), nullable=True)

    patients: Mapped["Patients"] = relationship(back_populates="appointments")
    worker: Mapped["Workers"] = relationship(back_populates="appointments")


class Insurance(Base):
    __tablename__ = "insurance"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str]

    patients: Mapped[list["Patients"]] = relationship(back_populates="insurance")


class PatientFamily(Base):
    __tablename__ = "family"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str]

    patients: Mapped[list["Patients"]] = relationship(back_populates="family")


# -----------------------------------------------------------------------------------------------------

class Offenses(Base):
    __tablename__ = "offenses"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str]
    demerit_points: Mapped[int]
    worker_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="CASCADE"))

    worker: Mapped["Workers"] = relationship(back_populates="offenses")
    __table_args__= (
        CheckConstraint("demerit_points>=0",name="CheckPoints"),
    )

class Workers(Base):
    __tablename__ = 'workers'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[str] = mapped_column(Enum(Roles))
    hashed_password: Mapped[str]
    gender:Mapped[str] = mapped_column(Enum(Gender))
    location_id:Mapped[PYUUID] = mapped_column(ForeignKey("locations.id"))

    location:Mapped["Location"] = relationship(back_populates="workers")
    appointments: Mapped[list["Appointments"]] = relationship(back_populates="worker")
    schedule: Mapped[list["Schedule"]] = relationship(back_populates="worker")
    vitals: Mapped[list["Vitals"]] = relationship(back_populates="worker")
    records: Mapped[list["Record"]] = relationship(back_populates="worker")
    offenses: Mapped[list["Offenses"]] = relationship(back_populates="worker")
    other_drug_history:Mapped[list["OtherDrugHistory"]] = relationship(back_populates="worker")
    @property
    def demerits(self) -> int:
        return sum(o.demerit_points for o in self.offenses)


class Permissions(Base):
    __tablename__ = "permissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(Enum(Roles))
    perm: Mapped[str]
    __table_args__ = (
        UniqueConstraint("role", "perm", name="UQ_role_perm"),
    )


class Schedule(Base):
    __tablename__ = 'schedule'
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

    worker_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="CASCADE"))

    worker: Mapped["Workers"] = relationship(back_populates="schedule")

    __table_args__ = (
        CheckConstraint("end_time>start_time","correct_time_constraint")
    )


class Record(Base):
    __tablename__ = "records"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date: Mapped[datetime]
    diagnosis: Mapped[str] = mapped_column(nullable=True)

    worker_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="SET NULL"), nullable=True)
    patient_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="RESTRICT"))

    patient: Mapped["Patients"] = relationship(back_populates="records")
    worker: Mapped["Workers"] = relationship(back_populates="records")
    vitals: Mapped[list["Vitals"]] = relationship(back_populates="record")
    drugs: Mapped[list["DrugsUsed"]] = relationship(back_populates="record")


class Vitals(Base):
    __tablename__ = "vitals"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    temp: Mapped[float]
    heart: Mapped[float]
    systolic_pressure: Mapped[int]
    diastolic_pressure: Mapped[int]

    patient_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("patients.id", ondelete="RESTRICT"))

    record_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"), nullable=True)
    worker_id: Mapped[PYUUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="SET NULL"), nullable=True)

    worker: Mapped["Workers"] = relationship(back_populates="vitals")
    record: Mapped["Record"] = relationship(back_populates="vitals")
    patient: Mapped["Patients"] = relationship(back_populates="vitals")


# -----------------------------------------------------------------------------------------------------

class DrugMaster(Base):
    __tablename__ = "pharmacy"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str]
    drug_code: Mapped[str]

    drug_typeid:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drug_type.id",ondelete="SET NULL"),nullable=True)

    @property
    def batches_number(self) -> int:
        return len(self.batches)
    
    drug_type:Mapped["DrugType"] = relationship(back_populates="pharmacy")
    batches:Mapped[list["Batches"]] = relationship(back_populates="pharmacy")
#i.e tablets, syrups
class DrugType(Base):
    __tablename__="drug_type"
    id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str]
    pharmacy:Mapped[list["DrugMaster"]] = relationship(back_populates="drug_type")
#i.e function based antibiotics etc
class DrugGroup(Base):
    __tablename__="drug_group"
    id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    name:Mapped[str]

    batch:Mapped[list["Batches"]] = relationship(back_populates="drug_group")


class Location(Base):
    __tablename__ = "locations"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    location_name:Mapped[str]

    old_location_history:Mapped[list["DrugLocation_TransferHistory"]] = relationship("Location",foreign_keys="[DrugLocation_TransferHistory.old_location_id]",back_populates="old_location")
    new_location_history:Mapped[list["DrugLocation_TransferHistory"]] = relationship("Location",foreign_keys="[DrugLocation_TransferHistory.new_location_id]",back_populates="new_location")

    inventory:Mapped[list["Inventory"]] = relationship(back_populates="location")
    workers:Mapped[list["Workers"]] = relationship(back_populates="location")

class Supplier(Base):
      __tablename__ = "suppliers"
      id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
      name:Mapped[str]
      batches:Mapped[list["Batches"]] = relationship(back_populates="supplier")

class Batches(Base):
    __tablename__ = "batches"
    id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    bulk_quantity:Mapped[int]
    conversion_rate:Mapped[int]
    expiry_date: Mapped[datetime]
    batch_number:Mapped[str]
    
    supplier_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),ForeignKey("suppliers.id",ondelete="SET NULL"),nullable=True)
    pharmacy_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),ForeignKey("pharmacy.id",ondelete="RESTRICT"))
    
    drug_groupid:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drug_group.id",ondelete="RESTRICT"))

    drug_group:Mapped["DrugGroup"] = relationship(back_populates="batch")
    
    supplier:Mapped[Supplier] = relationship(back_populates="batches")
    pharmacy:Mapped[DrugMaster]= relationship(back_populates="batches")
    inventory:Mapped[list["Inventory"]] = relationship(back_populates="batch")
    location_transfer_history :Mapped[list["DrugLocation_TransferHistory"]] = relationship(back_populates="batch")
    transfer_history :Mapped[list["Drug_TransferHistory"]] = relationship(back_populates="batch")
    __table_args__ = (
            CheckConstraint("bulk_quantity>=0",name="check_bulk_quantity"),
            CheckConstraint("conversion_rate>0",name="check_conversion"),
            UniqueConstraint("batch_number","pharmacy_id",name="no_same_batchNo_drug"),
            CheckConstraint("expiry_date>datetime.now()",name="expired_drug_blocking")
        )
class Inventory(Base):
    __tablename__ = "inventory"
    id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid4)
    quantity: Mapped[int] 
    location_id:Mapped[PYUUID]= mapped_column(UUID(as_uuid=True),ForeignKey("locations.id",ondelete="RESTRICT"))
    batch_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True),ForeignKey("batches.id",ondelete="CASCADE"))

    sender_history:Mapped[list["Drug_TransferHistory"]] = relationship("Inventory",foreign_keys="[Drug_TransferHistory.old_inventory_id]",back_populates="sender_inventory")
    receiver_history:Mapped[list["Drug_TransferHistory"]] = relationship("Inventory",foreign_keys="[Drug_TransferHistory.new_inventory_id]",back_populates="receiver_inventory")
    batch:Mapped[Batches] = relationship(back_populates="inventory")
    location:Mapped[Location] = relationship(back_populates="inventory")
    usage: Mapped[list["DrugsUsed"]] = relationship(back_populates="inventory")
    usage_other: Mapped[list["OtherDrugHistory"]] = relationship(back_populates="inventory")
    __table_args__ = (
        CheckConstraint("quantity>=0", name="check_retail_quantity"),
        UniqueConstraint("location_id","batch_id",name="no_double_batch_loc")
    )
class DrugsUsed(Base):
    __tablename__ = "drugs_used"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    quantity: Mapped[int]
    date: Mapped[datetime]
    inventory_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory.id", ondelete="RESTRICT"))
    record_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("records.id", ondelete="CASCADE"))

    inventory: Mapped["Inventory"] = relationship(back_populates="usage")
    record: Mapped["Record"] = relationship(back_populates="drugs")

class OtherDrugHistory(Base):
    __tablename__="drug_used_other"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    quantity: Mapped[int]
    memo:Mapped[str]
    date: Mapped[datetime]
    inventory_id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory.id", ondelete="RESTRICT"))
    worker_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id"))
    inventory: Mapped["Inventory"] = relationship(back_populates="usage_other")
    worker:Mapped["Workers"] = relationship(back_populates="other_drug_history")
class DrugLocation_TransferHistory(Base):
    __tablename__="drug_location_transfer_history"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    quantity: Mapped[int]
    old_location_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("locations.id"))
    new_location_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("locations.id"))
    batch_id :Mapped[PYUUID]=mapped_column(UUID(as_uuid=True), ForeignKey("batches.id"))
    worker_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id"))
    date:Mapped[datetime]
    old_location:Mapped["Location"] = relationship("Location",foreign_keys=[old_location_id],back_populates="old_location_history")
    new_location:Mapped["Location"] = relationship("Location",foreign_keys=[new_location_id],back_populates="new_location_history")
    batch:Mapped["Batches"] = relationship(back_populates="location_transfer_history")
    

class Drug_TransferHistory(Base):
    __tablename__="drug_transfer_history"
    id: Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    quantity: Mapped[int]
    old_inventory_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory.id"))
    new_inventory_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory.id"))
    batch_id :Mapped[PYUUID]=mapped_column(UUID(as_uuid=True), ForeignKey("batches.id"))
    worker_id:Mapped[PYUUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workers.id"))
    date:Mapped[datetime]
    sender_inventory:Mapped["Inventory"] = relationship("Inventory",foreign_keys=[old_inventory_id],back_populates="sender_history")
    receiver_inventory:Mapped["Inventory"] = relationship("Inventory",foreign_keys=[new_inventory_id],back_populates="receiver_history")
    batch:Mapped["Batches"] = relationship(back_populates="transfer_history")
# -----------------------------------------------------------------------------------------------------
