from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship


class Inventario(Serializable, Base):
    way = {'sucursal': {}, 'producto': {}}

    __tablename__ = 'negocio_inventario'

    id = Column(Integer, primary_key=True)

    fksucursal = Column(Integer, ForeignKey("negocio_sucursal.id"), nullable=True)
    fkproducto = Column(Integer, ForeignKey("negocio_producto.id"), nullable=True)
    cantidad = Column(Integer, default=0)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    sucursal = relationship("Sucursal")
    producto = relationship("Producto")
