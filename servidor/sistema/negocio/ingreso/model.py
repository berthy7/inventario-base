from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship


class Ingreso(Serializable, Base):
    way = {'sucursal': {}, 'detalle': {}}

    __tablename__ = 'negocio_ingreso'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(50), nullable=False, unique=True)
    fecha = Column(DateTime, nullable=True)
    fksucursal = Column(Integer, ForeignKey("negocio_sucursal.id"), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    sucursal = relationship("Sucursal")
    detalle = relationship("Ingreso_detalle", cascade="save-update, merge, delete, delete-orphan")

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = "----"
        else:
            aux['fecha'] = self.fecha.strftime("%d/%m/%Y %H:%M")
        return aux


class Ingreso_detalle(Serializable, Base):
    way = {'ingreso': {}, 'producto': {}}

    __tablename__ = 'negocio_ingreso_detalle'

    id = Column(Integer, primary_key=True)
    fkingreso = Column(Integer, ForeignKey("negocio_ingreso.id"), nullable=True)
    fkproducto = Column(Integer, ForeignKey("negocio_producto.id"), nullable=True)
    cantidad = Column(Integer, default=0)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    ingreso = relationship("Ingreso")
    producto = relationship("Producto")
