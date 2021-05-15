from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Table, Column, Text, ForeignKey, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import relationship


class Usuario(Serializable, Base):
    way = {'persona': {}, 'rol': {'modulos': {}}}

    __tablename__ = 'usuarios_usuario'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    token = Column(String(2000), nullable=True, default='Sin Token')
    fkpersona = Column(BigInteger, ForeignKey('usuarios_persona.id'), nullable=True)
    fkrol = Column(Integer, ForeignKey('usuarios_rol.id'), nullable=False)
    foto = Column(Text, nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    persona = relationship('Persona')
    rol = relationship('Rol')

    def get_dict(self, way=None):
        aux = super().get_dict(way)
        del(aux['password'])

        if aux['foto'] == 'None':
            aux['foto'] = ""

        return aux


Acceso = Table('usuarios_acceso', Base.metadata,
   Column('id', Integer, primary_key=True),
   Column('fkrol', Integer, ForeignKey('usuarios_rol.id')),
   Column('fkmodulo', Integer, ForeignKey('usuarios_modulo.id')))


class Modulo(Serializable, Base):
    way = {'roles': {}, 'children': {}}

    __tablename__ = 'usuarios_modulo'

    id = Column(Integer, primary_key=True)
    ruta = Column(String(100))
    titulo = Column(String(100), nullable=False)
    nombre = Column(String(100), nullable=False, unique=True)
    icono = Column(String(50), nullable=False, default='chevron_right')
    menu = Column(Boolean, nullable=False, default=True)
    fkmodulo = Column(Integer, ForeignKey('usuarios_modulo.id'))

    roles = relationship('Rol', secondary=Acceso)
    children = relationship('Modulo')
