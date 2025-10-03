# models.py
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from app.domain.dto.avionDTO import EstadoEnum

Base = declarative_base()

class Avion(Base):
    __tablename__ = "aviones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelo = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    aerolinea = Column(String, nullable=False)
    estado = Column(Enum(EstadoEnum), default=EstadoEnum.disponible)
    fecha_fabricacion = Column(DateTime, nullable=True)
