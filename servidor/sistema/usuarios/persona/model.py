from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship


class Persona(Serializable, Base):
    way = {'usuario': {}}

    __tablename__ = 'usuarios_persona'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=True)
    apellido = Column(String(255), nullable=True)
    ci = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    telefono = Column(String(255), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, nullable=False, default=True)

    usuario = relationship('Usuario')

    @hybrid_property
    def fullname(self):
        aux = ""
        if self.nombre is not None:
            aux += self.nombre
        else:
            aux = ""

        if self.apellido is not None:
            aux += " " + self.apellido
        else:
            aux = ""

        return aux

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['telefono'] == 'None':
            aux['telefono'] = ""

        if aux['ci'] == 'None':
            aux['ci'] = ""

        return aux
