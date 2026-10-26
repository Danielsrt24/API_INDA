from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Auditoria(SQLModel, table=True):
    __tablename__ = "auditoria"
    
    id_auditoria: Optional[int] = Field(default=None, primary_key=True)
    tabla_afectada: str = Field(max_length=50)
    registro_id: int
    accion: str = Field(max_length=10)  
    id_usuario: Optional[int] = Field(default=None, foreign_key="usuarios.id_usuario")
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    descripcion: Optional[str] = None