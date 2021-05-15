from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, Integer, String, Boolean


class Cliente(Serializable, Base):
    way = {}

    __tablename__ = 'negocio_cliente'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    nit = Column(String(50), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)
