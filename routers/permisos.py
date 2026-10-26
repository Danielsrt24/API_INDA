from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_db
from models.permiso import Permiso, PermisoCreate, PermisoUpdate, PermisoResponse

router = APIRouter(prefix="/permisos", tags=["Permisos"])

@router.get("/", response_model=List[PermisoResponse])
def listar_permisos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.exec(select(Permiso).where(Permiso.estado == True).offset(skip).limit(limit)).all()

@router.post("/", response_model=PermisoResponse, status_code=201)
def crear_permiso(data: PermisoCreate, db: Session = Depends(get_db)):
    nuevo = Permiso(**data.model_dump(), estado=True)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{permiso_id}", response_model=PermisoResponse)
def editar_permiso(permiso_id: int, data: PermisoUpdate, db: Session = Depends(get_db)):
    permiso = db.get(Permiso, permiso_id)
    if not permiso or not permiso.estado:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(permiso, key, value)
        
    db.add(permiso)
    db.commit()
    db.refresh(permiso)
    return permiso

@router.delete("/{permiso_id}")
def eliminar_permiso(permiso_id: int, db: Session = Depends(get_db)):
    permiso = db.get(Permiso, permiso_id)
    if not permiso or not permiso.estado:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    permiso.estado = False
    db.add(permiso)
    db.commit()
    return {"message": "Permiso desactivado"}