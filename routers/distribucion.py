from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_db
from models.distribucion import Distribucion, DistribucionCreate, DistribucionUpdate, DistribucionResponse

router = APIRouter(prefix="/distribucion", tags=["Distribución"])

@router.get("/", response_model=List[DistribucionResponse])
def listar_distribucion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.exec(select(Distribucion).where(Distribucion.estado == True).offset(skip).limit(limit)).all()

@router.post("/", response_model=DistribucionResponse, status_code=201)
def crear_distribucion(data: DistribucionCreate, db: Session = Depends(get_db)):
    stmt = select(Distribucion).where(
        Distribucion.id_profesor == data.id_profesor,
        Distribucion.id_materia == data.id_materia,
        Distribucion.id_seccion == data.id_seccion,
        Distribucion.estado == True
    )
    if db.exec(stmt).first():
        raise HTTPException(status_code=400, detail="Esta asignación ya existe")
    
    nuevo = Distribucion(**data.model_dump(), estado=True)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{dist_id}", response_model=DistribucionResponse)
def editar_distribucion(dist_id: int, data: DistribucionUpdate, db: Session = Depends(get_db)):
    dist = db.get(Distribucion, dist_id)
    if not dist or not dist.estado:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(dist, key, value)
        
    db.add(dist)
    db.commit()
    db.refresh(dist)
    return dist

@router.delete("/{dist_id}")
def eliminar_distribucion(dist_id: int, db: Session = Depends(get_db)):
    dist = db.get(Distribucion, dist_id)
    if not dist or not dist.estado:
        raise HTTPException(status_code=404, detail="Asignación no encontrada")
    dist.estado = False
    db.add(dist)
    db.commit()
    return {"message": "Asignación desactivada"}