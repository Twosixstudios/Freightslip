import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Setup
DB_FILE = "freightslip.db"
DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy ORM Model matching FreightSlip schema
class LoadRecord(Base):
    __tablename__ = "loads"

    id = Column(Integer, primary_key=True, index=True)
    broker_name = Column(String, nullable=True)
    load_number = Column(String, nullable=True)
    total_pay = Column(Float, default=0.0)
    line_haul_rate = Column(Float, default=0.0)
    fuel_surcharge = Column(Float, default=0.0)
    origin = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    equipment_type = Column(String, nullable=True)
    commodity = Column(String, nullable=True)
    total_miles = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Create tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

def save_load(rate_con):
    """Saves a parsed RateConfirmation schema object to SQLite."""
    db = SessionLocal()
    try:
        record = LoadRecord(
            broker_name=getattr(rate_con, "broker_name", None),
            load_number=getattr(rate_con, "load_number", None),
            total_pay=getattr(rate_con, "total_pay", 0.0) or 0.0,
            line_haul_rate=getattr(rate_con, "line_haul_rate", 0.0) or 0.0,
            fuel_surcharge=getattr(rate_con, "fuel_surcharge", 0.0) or 0.0,
            origin=getattr(rate_con, "origin", None),
            destination=getattr(rate_con, "destination", None),
            equipment_type=getattr(rate_con, "equipment_type", None),
            commodity=getattr(rate_con, "commodity", None),
            total_miles=getattr(rate_con, "total_miles", None),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_all_loads():
    """Retrieves all saved load records."""
    db = SessionLocal()
    try:
        return db.query(LoadRecord).order_by(LoadRecord.created_at.desc()).all()
    finally:
        db.close()