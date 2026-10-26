from sqlmodel import SQLModel, Field
from typing import Optional

class SeccionBase(SQLModel):
    nombre: str = Field(max_length=100)
    nivel: Optional[str] = Field(default=None, max_length=50)
    letra: Optional[str] = Field(default=None, max_length=10)

class SeccionCreate(SeccionBase):
    pass

class SeccionUpdate(SQLModel):
    nombre: Optional[str] = None
    nivel: Optional[str] = None
    letra: Optional[str] = None

class SeccionResponse(SeccionBase):
    id_seccion: int
    estado: bool

    class Config:
        from_attributes = True

class Seccion(SeccionBase, table=True):
    __tablename__ = "secciones"
    
    id_seccion: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)
    
    __table_args__ = {"extend_existing": True}