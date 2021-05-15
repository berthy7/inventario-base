from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship


class Salida(Serializable, Base):
    way = {'cliente': {}, 'sucursal': {}, 'detalle': {}}

    __tablename__ = 'negocio_salida'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(50), nullable=False, unique=True)
    fecha = Column(DateTime, nullable=True)
    fksucursal = Column(Integer, ForeignKey("negocio_sucursal.id"), nullable=True)
    fkcliente = Column(Integer, ForeignKey("negocio_cliente.id"), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    sucursal = relationship("Sucursal")
    cliente = relationship("Cliente")
    detalle = relationship("Salida_detalle", cascade="save-update, merge, delete, delete-orphan")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = "----"
        else:
            aux['fecha'] = self.fecha.strftime("%d/%m/%Y %H:%M")
        return aux



class Salida_detalle(Serializable, Base):
    way = {'ingreso': {}, 'producto': {}}

    __tablename__ = 'negocio_salida_detalle'

    id = Column(Integer, primary_key=True)
    fksalida = Column(Integer, ForeignKey("negocio_salida.id"), nullable=True)
    fkproducto = Column(Integer, ForeignKey("negocio_producto.id"), nullable=True)
    cantidad = Column(Integer, default=0)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    salida = relationship("Salida")
    producto = relationship("Producto")
