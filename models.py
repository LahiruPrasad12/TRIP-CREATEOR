from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from sqlalchemy.sql import func  # for current timestamp
from datetime import datetime
import pytz
from sqlalchemy.orm import validates



colombo_tz = pytz.timezone('Asia/Colombo')


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    num_of_passengers = Column(Integer, nullable=False)
    amount_per_passenger = Column(Float, nullable=False)
    from_location = Column("from", String, nullable=False)
    to = Column(String, nullable=False)
    company_id = Column(Integer, nullable=False)
    route_id = Column(Integer, nullable=False)
    url = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(colombo_tz), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(colombo_tz), onupdate=lambda: datetime.now(colombo_tz), nullable=False)

    @validates('created_at', 'updated_at')
    def convert_to_colombo_time(self, key, value):
        return value.astimezone(colombo_tz) if value else value
