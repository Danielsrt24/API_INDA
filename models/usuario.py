from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
   # PRUEBA DE GIT DANI
class UsuarioBase(SQLModel):
    username: str = Field(index=True, unique=True, max_length=50)
    nombre: str = Field(max_length=150)
    rol: str = Field(default="Profesor", max_length=20)
    email: Optional[str] = Field(default=None, max_length=100)

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=6, max_length=128)

class UsuarioUpdate(SQLModel):
    username: Optional[str] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=6, max_length=128)

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    estado: bool
    fecha_registro: Optional[datetime] = None

    class Config:
        from_attributes = True

class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"
    
    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(max_length=255)
    estado: bool = Field(default=True)
    
    fecha_registro: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    __table_args__ = {"extend_existing": True}