from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class ProfesorBase(SQLModel):
    nombre: str = Field(max_length=150)
    email: Optional[str] = Field(default=None, max_length=100)

class ProfesorCreate(ProfesorBase):
    pass

class ProfesorUpdate(SQLModel):
    nombre: Optional[str] = None
    email: Optional[str] = None

class ProfesorResponse(ProfesorBase):
    id_profesor: int
    estado: bool
    fecha_creacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class Profesor(ProfesorBase, table=True):
    __tablename__ = "profesores"
    
    id_profesor: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)
    
    fecha_creacion: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    __table_args__ = {"extend_existing": True}