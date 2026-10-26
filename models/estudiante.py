from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Estudiante(SQLModel, table=True):
    __tablename__ = "estudiantes"
    
    id_estudiante: Optional[int] = Field(default=None, primary_key=True)
    cedula: str = Field(index=True, unique=True, max_length=20)
    nombre: str = Field(max_length=150)
    email: Optional[str] = Field(default=None, max_length=100)
    estado: bool = Field(default=True)
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))