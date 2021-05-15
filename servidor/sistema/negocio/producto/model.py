from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, String, Boolean, BigInteger, Float


class Producto(Serializable, Base):
    way = {}

    __tablename__ = 'negocio_producto'

    id = Column(BigInteger, primary_key=True)
    codigo = Column(String(50), nullable=False)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=False)
    precio = Column(Float, nullable=False)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)
