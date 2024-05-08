from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from ..database import Base


class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    