from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.domain.dto.avionDTO import AvionDTO, EstadoEnum
from app.persistence.database.database import SessionLocal
from app.persistence.mapper.AvionMapper import dto_a_entidad, entidad_a_dto
from app.persistence.serviceImpl.serviceAvion import ServiceAvion
from app.exception.avion_exceptions import AvionNotFoundError, AvionValidationError

router = APIRouter(prefix="/aviones", tags=["Aviones"])

def get_db():
    """Dependency para obtener la sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_service(db: Session = Depends(get_db)):
    """Dependency para obtener el servicio de avión"""
    return ServiceAvion(db)


# Crear un avión
@router.post("/", response_model=AvionDTO, status_code=status.HTTP_201_CREATED)
def crear_avion(avion_dto: AvionDTO, service: ServiceAvion = Depends(get_service)):
    """
    Crear un nuevo avión
    
    - **modelo**: Modelo del avión (requerido)
    - **capacidad**: Capacidad de pasajeros (requerido)
    - **aerolinea**: Aerolínea propietaria (requerido)
    - **estado**: Estado del avión (opcional, por defecto: disponible)
    - **fecha_fabricacion**: Fecha de fabricación (opcional)
    """
    try:
        # DTO -> Entidad
        avion_entidad = dto_a_entidad(avion_dto)
        avion_guardado = service.save(avion_entidad)
        # Entidad -> DTO
        return entidad_a_dto(avion_guardado)
    except Exception as e:
        raise AvionValidationError(f"Error al crear avión: {str(e)}")


# Obtener un avión por ID
@router.get("/{avion_id}", response_model=AvionDTO)
def obtener_avion(avion_id: int, service: ServiceAvion = Depends(get_service)):
    """
    Obtener un avión por su ID
    
    - **avion_id**: ID único del avión
    """
    avion = service.getAvion(avion_id)
    if not avion:
        raise AvionNotFoundError(avion_id)
    return entidad_a_dto(avion)


# Obtener todos los aviones
@router.get("/", response_model=List[AvionDTO])
def obtener_todos_aviones(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros a retornar"),
    service: ServiceAvion = Depends(get_service)
):
    """
    Obtener todos los aviones con paginación
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar
    """
    aviones = service.getAllAviones(skip, limit)
    return [entidad_a_dto(avion) for avion in aviones]


# Obtener aviones por estado
@router.get("/estado/{estado}", response_model=List[AvionDTO])
def obtener_aviones_por_estado(
    estado: str, 
    service: ServiceAvion = Depends(get_service)
):
    """
    Obtener aviones por estado
    
    - **estado**: Estado del avión (disponible, mantenimiento, fuera_de_servicio)
    """
    if estado not in [e.value for e in EstadoEnum]:
        raise AvionValidationError(f"Estado inválido: {estado}")
    
    aviones = service.getAvionByEstado(estado)
    return [entidad_a_dto(avion) for avion in aviones]


# Obtener aviones por aerolínea
@router.get("/aerolinea/{aerolinea}", response_model=List[AvionDTO])
def obtener_aviones_por_aerolinea(
    aerolinea: str, 
    service: ServiceAvion = Depends(get_service)
):
    """
    Obtener aviones por aerolínea
    
    - **aerolinea**: Nombre de la aerolínea
    """
    aviones = service.getAvionByAerolinea(aerolinea)
    return [entidad_a_dto(avion) for avion in aviones]


# Obtener aviones por fecha de fabricación
@router.get("/fecha-fabricacion/{fecha_fabricacion}", response_model=List[AvionDTO])
def obtener_aviones_por_fecha_fabricacion(
    fecha_fabricacion: datetime, 
    service: ServiceAvion = Depends(get_service)
):
    """
    Obtener aviones por fecha de fabricación
    
    - **fecha_fabricacion**: Fecha de fabricación en formato ISO (YYYY-MM-DD)
    """
    aviones = service.getAvionByFechaFabricacion(fecha_fabricacion)
    return [entidad_a_dto(avion) for avion in aviones]


# Actualizar un avión
@router.put("/{avion_id}", response_model=AvionDTO)
def actualizar_avion(
    avion_id: int, 
    avion_dto: AvionDTO, 
    service: ServiceAvion = Depends(get_service)
):
    """
    Actualizar un avión existente
    
    - **avion_id**: ID del avión a actualizar
    - **avion_dto**: Datos actualizados del avión
    """
    # Verificar que el avión existe
    avion_existente = service.getAvion(avion_id)
    if not avion_existente:
        raise AvionNotFoundError(avion_id)
    
    # DTO -> Entidad
    avion_actualizado = dto_a_entidad(avion_dto)
    avion_actualizado.id = avion_id  # Asegurar que el ID sea correcto
    
    avion_modificado = service.edit(avion_id, avion_actualizado)
    return entidad_a_dto(avion_modificado)


# Eliminar un avión
@router.delete("/{avion_id}", response_model=AvionDTO)
def eliminar_avion(avion_id: int, service: ServiceAvion = Depends(get_service)):
    """
    Eliminar un avión por ID
    
    - **avion_id**: ID del avión a eliminar
    """
    avion = service.delete(avion_id)
    if not avion:
        raise AvionNotFoundError(avion_id)
    return entidad_a_dto(avion)
