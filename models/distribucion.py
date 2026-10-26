from sqlmodel import SQLModel, Field
from typing import Optional

class DistribucionBase(SQLModel):
    id_profesor: int
    id_materia: int = Field(foreign_key="materias.id_materia")
    id_seccion: int = Field(foreign_key="secciones.id_seccion")
    horas_semanales: int = Field(default=0)

class DistribucionCreate(DistribucionBase):
    pass

class DistribucionUpdate(SQLModel):
    id_profesor: Optional[int] = None
    id_materia: Optional[int] = None
    id_seccion: Optional[int] = None
    horas_semanales: Optional[int] = None

class DistribucionResponse(DistribucionBase):
    id_distribucion: int
    estado: bool

    class Config:
        from_attributes = True

class Distribucion(DistribucionBase, table=True):
    __tablename__ = "distribucion"
    id_distribucion: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)

    __table_args__ = {"extend_existing": True}