from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_db
from models.seccion import Seccion, SeccionCreate, SeccionUpdate, SeccionResponse

router = APIRouter(prefix="/secciones", tags=["Secciones"])

@router.get("/", response_model=List[SeccionResponse])
def listar_secciones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.exec(
        select(Seccion).where(Seccion.estado == True).offset(skip).limit(limit)
    ).all()

@router.get("/{seccion_id}", response_model=SeccionResponse)
def obtener_seccion(seccion_id: int, db: Session = Depends(get_db)):
    seccion = db.get(Seccion, seccion_id)
    if not seccion or not seccion.estado:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion

@router.post("/", response_model=SeccionResponse, status_code=201)
def crear_seccion(data: SeccionCreate, db: Session = Depends(get_db)):
    stmt = select(Seccion).where(
        Seccion.nombre == data.nombre,
        Seccion.grado == data.grado,
        Seccion.estado == True
    )
    if db.exec(stmt).first():
        raise HTTPException(status_code=400, detail="Ya existe una sección con ese nombre y grado")
    
    nuevo = Seccion(**data.model_dump(), estado=True)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{seccion_id}", response_model=SeccionResponse)
def editar_seccion(seccion_id: int, data: SeccionUpdate, db: Session = Depends(get_db)):
    seccion = db.get(Seccion, seccion_id)
    if not seccion or not seccion.estado:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(seccion, key, value)
        
    db.add(seccion)
    db.commit()
    db.refresh(seccion)
    return seccion

@router.delete("/{seccion_id}")
def eliminar_seccion(seccion_id: int, db: Session = Depends(get_db)):
    seccion = db.get(Seccion, seccion_id)
    if not seccion or not seccion.estado:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    seccion.estado = False
    db.add(seccion)
    db.commit()
    return {"message": "Sección desactivada"}