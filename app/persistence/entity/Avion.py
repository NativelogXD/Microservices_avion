# models.py
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class EstadoAvionEnum(str, enum.Enum):
    disponible = "disponible"
    mantenimiento = "mantenimiento"
    fuera_de_servicio = "fuera_de_servicio"

class Avion(Base):
    __tablename__ = "aviones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    modelo = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    aerolinea = Column(String, nullable=False)
    estado = Column(Enum(EstadoAvionEnum), default=EstadoAvionEnum.disponible)
    fecha_fabricacion = Column(DateTime, nullable=True)
