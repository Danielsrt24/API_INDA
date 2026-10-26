from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from database import get_db
from models.usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from core.helper import hash_password

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.exec(
        select(Usuario).where(Usuario.estado == True).offset(skip).limit(limit)
    ).all()

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario or not usuario.estado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    if db.exec(select(Usuario).where(Usuario.username == data.username)).first():
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    nuevo_usuario = Usuario(
        username=data.username,
        password_hash=hash_password(data.password),
        nombre=data.nombre,
        rol=data.rol,
        email=data.email,
        estado=True
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    
    if data.rol == "Profesor":
        try:
            from models.profesor import Profesor
            
            cedula_temporal = data.username
            
            profesor_existente = db.exec(
                select(Profesor).where(Profesor.cedula == cedula_temporal)
            ).first()
            
            if not profesor_existente:
                nuevo_profesor = Profesor(
                    cedula=cedula_temporal,
                    nombre=data.nombre,
                    email=data.email,
                    telefono=None,
                    estado=True,
                )
                db.add(nuevo_profesor)
                db.commit()
                print(f"✅ Profesor '{data.nombre}' creado automáticamente")
            else:
                print(f"⚠️ Ya existía un profesor con cédula '{cedula_temporal}'")
        except Exception as e:
            print(f"⚠️ No se pudo crear el profesor automáticamente: {str(e)}")
    
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario or not usuario.estado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if data.nombre: usuario.nombre = data.nombre
    if data.rol: usuario.rol = data.rol
    if data.email: usuario.email = data.email
    if data.password:
        usuario.password_hash = hash_password(data.password)
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.get(Usuario, usuario_id)
    if not usuario or not usuario.estado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    usuario.estado = False
    db.add(usuario)
    db.commit()
    
    return {"message": "Usuario desactivado"}