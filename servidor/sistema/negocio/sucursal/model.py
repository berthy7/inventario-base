from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Sucursal(Serializable, Base):
    way = {'empresa': {}}

    __tablename__ = 'negocio_sucursal'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    fkempresa = Column(Integer, ForeignKey("negocio_empresa.id"), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    empresa = relationship("Empresa")
