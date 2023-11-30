import datetime
import logging
from typing import List

from sqlalchemy import String, Integer, Date, create_engine, ForeignKey, UniqueConstraint, select 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

class HRDBBase(DeclarativeBase):    
    pass
    
class Employee(HRDBBase):
    __tablename__='hrms_employees'
    id : Mapped[int] = mapped_column(primary_key=True)
    fname : Mapped[str] = mapped_column(String(50))
    lname : Mapped[str] = mapped_column(String(50))
    email : Mapped[str] = mapped_column(String(100))
    phone : Mapped[str] = mapped_column(String(100))
    designation_id : Mapped[str] = mapped_column(ForeignKey('hrms_designation.id'))
    designation : Mapped['Designation'] = relationship(back_populates = "employees")

class Designation(HRDBBase):
    __tablename__='hrms_designation'
    id : Mapped[int] = mapped_column(primary_key=True)
    designation_name : Mapped[str] = mapped_column(String(100))
    max_leaves : Mapped[int] = mapped_column(Integer(100))
    employees : Mapped ["Employee"] = relationship(back_populates ="designation")

class Leave(HRDBBase):
    __tablename__ = "hrms_leaves"
    __table_args__ = (        
        UniqueConstraint("employee_id", "date"),
        )
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(Date())
    employee_id: Mapped[int] = mapped_column(ForeignKey('hrms_employees.id'))
    reason: Mapped[str] =  mapped_column(String(200))

def create_all(db_uri):
    logger = logging.getLogger("HR")
    engine = create_engine(db_uri)
    HRDBBase.metadata.create_all(engine)
    logger.info("Created database")

def get_session(db_uri):
    engine = create_engine(db_uri)
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
