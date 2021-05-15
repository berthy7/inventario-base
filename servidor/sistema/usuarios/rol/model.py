from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from servidor.sistema.usuarios.usuario.model import Acceso


class Rol(Serializable, Base):
    way = {'usuarios': {}, 'modulos': {}}

    __tablename__ = 'usuarios_rol'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(500), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    usuarios = relationship('Usuario')
    modulos = relationship('Modulo', secondary=Acceso)
