from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class EstadoEnum(str, Enum):
    disponible = "disponible"
    mantenimiento = "mantenimiento"
    fuera_de_servicio = "fuera_de_servicio"

class AvionDTO(BaseModel):
    id: Optional[int] = None
    modelo: str
    capacidad: int
    aerolinea: str
    estado: EstadoEnum = EstadoEnum.disponible
    fecha_fabricacion: Optional[datetime] = None
