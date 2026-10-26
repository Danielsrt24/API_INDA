from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class MateriaBase(SQLModel):
    codigo: str = Field(max_length=20, unique=True)
    nombre: str = Field(max_length=150)
    creditos: int = Field(default=0)

class MateriaCreate(MateriaBase):
    pass

class MateriaUpdate(SQLModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    creditos: Optional[int] = None

class MateriaResponse(MateriaBase):
    id_materia: int
    estado: bool
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class Materia(MateriaBase, table=True):
    __tablename__ = "materias"
    
    id_materia: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)
    fecha_creacion: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    __table_args__ = {"extend_existing": True}