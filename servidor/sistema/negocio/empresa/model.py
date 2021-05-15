from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger


class Empresa(Serializable, Base):
    way = {}

    __tablename__ = 'negocio_empresa'

    id = Column(BigInteger, primary_key=True)
    nombre = Column(String(50), nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)
