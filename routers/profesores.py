from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from database import get_db
from models.profesor import Profesor, ProfesorCreate, ProfesorUpdate, ProfesorResponse

router = APIRouter(prefix="/profesores", tags=["Profesores"])

@router.get("/", response_model=List[ProfesorResponse])
def listar_profesores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.exec(
        select(Profesor).where(Profesor.estado == True).offset(skip).limit(limit)
    ).all()

@router.get("/{profesor_id}", response_model=ProfesorResponse)
def obtener_profesor(profesor_id: int, db: Session = Depends(get_db)):
    profesor = db.get(Profesor, profesor_id)
    if not profesor or not profesor.estado:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

@router.post("/", response_model=ProfesorResponse, status_code=201)
def crear_profesor(data: ProfesorCreate, db: Session = Depends(get_db)):
    if db.exec(select(Profesor).where(Profesor.cedula == data.cedula)).first():
        raise HTTPException(status_code=400, detail="Ya existe un profesor con esa cédula")
    
    nuevo = Profesor(
        cedula=data.cedula,
        nombre=data.nombre,
        email=data.email,
        telefono=data.telefono,
        estado=True
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.put("/{profesor_id}", response_model=ProfesorResponse)
def editar_profesor(profesor_id: int, data: ProfesorUpdate, db: Session = Depends(get_db)):
    profesor = db.get(Profesor, profesor_id)
    if not profesor or not profesor.estado:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    if data.cedula: profesor.cedula = data.cedula
    if data.nombre: profesor.nombre = data.nombre
    if data.email: profesor.email = data.email
    if data.telefono: profesor.telefono = data.telefono
    
    db.add(profesor)
    db.commit()
    db.refresh(profesor)
    return profesor

@router.delete("/{profesor_id}")
def eliminar_profesor(profesor_id: int, db: Session = Depends(get_db)):
    profesor = db.get(Profesor, profesor_id)
    if not profesor or not profesor.estado:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    profesor.estado = False
    db.add(profesor)
    db.commit()
    
    return {"message": "Profesor desactivado"}