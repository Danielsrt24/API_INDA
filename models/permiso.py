from sqlmodel import SQLModel, Field
from typing import Optional

class PermisoBase(SQLModel):
    rol: str = Field(max_length=20)
    modulo: str = Field(max_length=50)
    puede_ver: bool = Field(default=True)
    puede_crear: bool = Field(default=False)
    puede_editar: bool = Field(default=False)
    puede_eliminar: bool = Field(default=False)

class PermisoCreate(PermisoBase):
    pass

class PermisoUpdate(SQLModel):
    puede_ver: Optional[bool] = None
    puede_crear: Optional[bool] = None
    puede_editar: Optional[bool] = None
    puede_eliminar: Optional[bool] = None

class PermisoResponse(PermisoBase):
    id_permiso: int

    class Config:
        from_attributes = True

class Permiso(PermisoBase, table=True):
    __tablename__ = "permisos"
    id_permiso: Optional[int] = Field(default=None, primary_key=True)
    estado: bool = Field(default=True)