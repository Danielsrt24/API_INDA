from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import time

class HorarioBase(SQLModel):
    id_distribucion: int = Field(foreign_key="distribucion.id_distribucion")
    dia: str = Field(max_length=10)
    hora_inicio: time
    hora_fin: time
    aula: Optional[str] = Field(default=None, max_length=20)

class HorarioCreate(HorarioBase):
    pass

class HorarioUpdate(SQLModel):
    dia: Optional[str] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    aula: Optional[str] = None

class HorarioResponse(HorarioBase):
    id_horario: int
    estado: bool
    class Config:
        from_attributes = True

class Horario(HorarioBase, table=True):
    __tablename__ = "horario"
    id_horario: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)
    __table_args__ = {"extend_existing": True}